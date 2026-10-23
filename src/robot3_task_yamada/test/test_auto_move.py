#!/usr/bin/env python3
"""Run after sourcing ROS: python3 -m unittest discover -s test."""
import importlib.util
import math
from pathlib import Path
import unittest
from unittest.mock import Mock, patch
import xml.etree.ElementTree as ET

import rospy
from geometry_msgs.msg import Point, TransformStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import tf2_ros

PACKAGE = Path(__file__).resolve().parents[1]


class LoopStopped(Exception):
    pass


class ControllerTest(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location(
            "auto_move_under_test", PACKAGE / "src/auto_move.py")
        self.node = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.node)
        self.pub = Mock()
        self.rate = Mock()
        self.patch(self.node.rospy, "is_shutdown", return_value=False)
        self.patch(self.node.rospy, "Rate", return_value=self.rate)
        self.patch(self.node.time, "sleep", side_effect=self.run_main)

    def patch(self, obj, name, **kwargs):
        patcher = patch.object(obj, name, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def scan(self, ranges):
        scan = LaserScan()
        scan.header.frame_id = "base_scan"
        scan.header.stamp = rospy.Time(1734171840)
        scan.range_min, scan.range_max = 0.0, 3.5
        scan.angle_min, scan.angle_increment = -math.pi / 2, math.pi / 2
        scan.ranges = ranges
        return scan

    def ready(self, distance=1.0, speed=0.0):
        self.node.goal = Point(x=distance, y=0.0)
        odom = Odometry()
        odom.header.frame_id = "odom"
        odom.pose.pose.orientation.w = 1.0
        odom.twist.twist.linear.x = speed
        self.node.odom_callback(odom)

    def last_command(self):
        return self.pub.publish.call_args.args[0]

    def run_main(self, *_):
        rate = Mock()

        def tick():
            self.rate.sleep()
            if not self.node.moving:
                raise LoopStopped
            if rate.sleep.call_count > 100:
                self.fail("Main loop failed to finish")

        rate.sleep.side_effect = tick
        with patch.multiple(
                self.node.rospy, init_node=Mock(), Subscriber=Mock(), Service=Mock(),
                on_shutdown=Mock(), Publisher=Mock(return_value=self.pub),
                Rate=Mock(return_value=rate)), \
                patch.object(self.node.tf2_ros, "Buffer"), \
                patch.object(self.node.tf2_ros, "TransformListener"):
            with self.assertRaises(LoopStopped):
                self.node.main()

    def assert_stopped(self):
        command = self.last_command()
        self.assertEqual((command.linear.x, command.angular.z), (0.0, 0.0))
        self.assertFalse(self.node.moving)

    def test_invalid_ranges_and_scan_to_odom_geometry(self):
        scan = self.scan([0.0, math.inf, 1.0, math.nan, -1.0, 0.5, 4.0])
        transform = TransformStamped()
        transform.transform.translation.x = 2.0
        transform.transform.translation.y = 3.0
        transform.transform.rotation.z = math.sin(math.pi / 4)
        transform.transform.rotation.w = math.cos(math.pi / 4)
        buffer = tf2_ros.BufferInterface()
        buffer.lookup_transform = Mock(return_value=transform)
        self.node.scan_callback(scan, buffer)
        self.assertAlmostEqual(self.node.goal.x, 2.0)
        self.assertAlmostEqual(self.node.goal.y, 3.5)
        self.assertEqual(buffer.lookup_transform.call_args.args[:3],
                         ("odom", "base_scan", scan.header.stamp))

    def test_all_invalid_ranges_stop_and_report_reason(self):
        self.ready()
        buffer = Mock()
        self.node.scan_callback(self.scan([0.0, math.inf, math.nan, -1.0, 4.0]), buffer)
        buffer.transform.assert_not_called()
        response = self.node.goto_closest(None)
        self.assertFalse(response.success)
        self.assertEqual(response.message, "No scan, TF or odometry.")
        self.assert_stopped()

    def test_below_minimum_range_is_excluded(self):
        scan = self.scan([0.05])
        scan.range_min = 0.1
        self.node.scan_callback(scan, Mock())
        self.assertIsNone(self.node.goal)

    def test_tf_error_clears_previous_goal(self):
        self.ready()
        buffer = Mock()
        buffer.transform.side_effect = tf2_ros.ExtrapolationException("missing TF")
        self.node.scan_callback(self.scan([1.0]), buffer)
        response = self.node.goto_closest(None)
        self.assertFalse(response.success)
        self.assertEqual(response.message, "No scan, TF or odometry.")
        self.assert_stopped()

    def test_startup_waits_for_service(self):
        self.ready()
        self.run_main()
        self.assert_stopped()
        self.assertFalse(self.node.moving)

    def test_missing_odometry_reports_reason(self):
        self.node.goal = Point(x=1.0, y=0.0)
        response = self.node.goto_closest(None)
        self.assertFalse(response.success)
        self.assertEqual(response.message, "No scan, TF or odometry.")
        self.assert_stopped()

    def test_service_moves_waits_for_stop_and_allows_another_request(self):
        self.ready()

        def tick():
            step = self.rate.sleep.call_count
            if step == 1:
                self.assertEqual(self.last_command().linear.x, 0.25)
                self.assertFalse(self.node.goto_closest(None).success)
                self.ready(distance=0.31, speed=0.05)
            elif step == 2:
                self.assertEqual(self.last_command().linear.x, 0.0)
                self.ready(distance=0.31)
            elif step == 3:
                self.assertEqual(self.last_command().linear.x, 0.0)
            elif step > 4:
                self.fail("Service failed to finish after measured stop")

        self.rate.sleep.side_effect = tick
        self.assertTrue(self.node.goto_closest(None).success)
        self.assert_stopped()
        # A moved target stays idle until the next call.
        published = self.pub.publish.call_count
        self.ready(distance=2.0)
        self.assertEqual(self.pub.publish.call_count, published)
        self.node.goal = None
        self.rate.sleep.side_effect = None
        self.assertFalse(self.node.goto_closest(None).success)
        self.assert_stopped()

    def test_turn_before_advancing(self):
        self.ready()
        self.node.goal = Point(x=0.0, y=1.0)

        def tick():
            if self.rate.sleep.call_count == 1:
                command = self.last_command()
                self.assertEqual(command.linear.x, 0.0)
                self.assertEqual(command.angular.z, 0.5)
                self.ready(distance=0.31)
            elif self.rate.sleep.call_count > 3:
                self.fail("Service failed to finish")

        self.rate.sleep.side_effect = tick
        self.assertTrue(self.node.goto_closest(None).success)
        self.assert_stopped()

    def test_shutdown_returns_service_failure(self):
        self.ready()
        self.patch(self.node.rospy, "is_shutdown", return_value=True)
        self.assertFalse(self.node.goto_closest(None).success)
        self.assertFalse(self.node.moving)

    def test_real_launch_has_only_controller_and_rviz(self):
        launch = ET.parse(PACKAGE / "launch/turtlebot3_real.launch").getroot()
        self.assertEqual({node.attrib["pkg"] for node in launch.findall("node")},
                         {"rviz", "robot3_task_yamada"})
        self.assertFalse(launch.findall("include"))
        self.assertEqual(launch.find("param[@name='use_sim_time']").attrib["value"], "false")


if __name__ == "__main__":
    unittest.main()
