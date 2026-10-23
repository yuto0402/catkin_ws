#!/usr/bin/env python3
import math
import time

import rospy
import tf2_geometry_msgs
import tf2_ros
from geometry_msgs.msg import PointStamped, Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_srvs.srv import Trigger, TriggerResponse
from tf.transformations import euler_from_quaternion

goal = None
robot_odom = None
moving = False
response = None


def scan_callback(scan, tf_buffer):
    global goal
    closest = math.inf

    for i, distance in enumerate(scan.ranges):
        if not math.isfinite(distance) or distance <= 0.0:
            continue
        if distance < scan.range_min or distance > scan.range_max:
            continue
        if distance < closest:
            closest = distance
            angle = scan.angle_min + i * scan.angle_increment

    if closest == math.inf:
        goal = None
        return

    point = PointStamped()
    point.header = scan.header
    point.point.x = closest * math.cos(angle)
    point.point.y = closest * math.sin(angle)
    try:
        point = tf_buffer.transform(point, "odom", rospy.Duration(0.1))
        goal = point.point
    except tf2_ros.TransformException:
        goal = None


def odom_callback(message):
    global robot_odom
    robot_odom = message


def goto_closest(_):
    global moving, response
    if moving:
        return TriggerResponse(success=False, message="Already moving.")

    response = None
    moving = True
    while moving and not rospy.is_shutdown():
        time.sleep(0.05)

    moving = False
    if response is None:
        return TriggerResponse(success=False, message="Node is shutting down.")
    return response


def main():
    global moving, response
    rospy.init_node("auto_move")
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    tf_buffer = tf2_ros.Buffer()
    tf_listener = tf2_ros.TransformListener(tf_buffer)
    rospy.Subscriber("/scan", LaserScan, scan_callback, callback_args=tf_buffer, queue_size=1)
    rospy.Subscriber("/odom", Odometry, odom_callback, queue_size=1)
    service = rospy.Service("/goto_closest", Trigger, goto_closest)
    rospy.on_shutdown(lambda: pub.publish(Twist()))
    rate = rospy.Rate(20)

    while not rospy.is_shutdown():
        command = Twist()
        target = goal
        odom = robot_odom

        if moving:
            if target is None or odom is None:
                response = TriggerResponse(success=False, message="No scan, TF or odometry.")
            else:
                position = odom.pose.pose.position
                q = odom.pose.pose.orientation
                yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])[2]
                velocity = odom.twist.twist
                dx = target.x - position.x
                dy = target.y - position.y
                remaining = math.hypot(dx, dy) - 0.3

                if remaining > 0.02:
                    angle = math.atan2(dy, dx) - yaw
                    angle = math.atan2(math.sin(angle), math.cos(angle))
                    command.angular.z = max(-0.5, min(0.5, angle))
                    if abs(angle) <= math.pi / 4:
                        command.linear.x = min(0.25, 0.5 * remaining)
                elif (math.hypot(velocity.linear.x, velocity.linear.y) < 0.01
                      and abs(velocity.angular.z) < 0.02):
                    response = TriggerResponse(success=True, message="Stopped.")

        pub.publish(command)
        if moving and response is not None:
            moving = False
        rate.sleep()


if __name__ == "__main__":
    main()
