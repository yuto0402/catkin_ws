#!/usr/bin/env python3
import math
import threading

import rospy
import tf2_geometry_msgs
import tf2_ros
from geometry_msgs.msg import PointStamped, Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_srvs.srv import Trigger, TriggerResponse
from tf.transformations import euler_from_quaternion

goal = None
robot_pose = None
robot_velocity = None
active_request = None
request_lock = threading.Lock()

K_ANGLE = 1.0
K_DISTANCE = 0.5
MAX_LINEAR_SPEED = 0.25
MAX_ANGULAR_SPEED = 0.5
STOP_DISTANCE = 0.3
GOAL_TOLERANCE = 0.02
SCAN_TIMEOUT = 1.0
STOP_SETTLE_TIME = 0.3


def scan_callback(message, tf_buffer):
    global goal
    nearest = min(
        ((distance, i) for i, distance in enumerate(message.ranges)
         if math.isfinite(distance)
         and message.range_min <= distance <= message.range_max),
        default=None,
    )
    if nearest is None:
        goal = None
        return

    distance, index = nearest
    angle = message.angle_min + index * message.angle_increment
    point = PointStamped()
    point.header = message.header
    point.point.x = distance * math.cos(angle)
    point.point.y = distance * math.sin(angle)

    try:
        transform = tf_buffer.lookup_transform(
            "odom", point.header.frame_id, point.header.stamp,
            rospy.Duration(0.1),
        )
        point_odom = tf2_geometry_msgs.do_transform_point(point, transform)
    except (tf2_ros.LookupException, tf2_ros.ConnectivityException,
            tf2_ros.ExtrapolationException) as error:
        goal = None
        rospy.logwarn_throttle(5.0, "Cannot transform scan to odom: %s", error)
        return

    goal = (point_odom.point.x, point_odom.point.y, message.header.stamp)


def odom_callback(message):
    global robot_pose, robot_velocity
    position = message.pose.pose.position
    q = message.pose.pose.orientation
    _, _, yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])
    robot_pose = (position.x, position.y, yaw)
    velocity = message.twist.twist
    robot_velocity = (math.hypot(velocity.linear.x, velocity.linear.y),
                      abs(velocity.angular.z))


def goto_closest(_):
    global active_request
    with request_lock:
        if active_request is not None:
            return TriggerResponse(success=False, message="Robot is already moving.")
        request = {"done": threading.Event(), "response": None,
                   "stopped_since": None}
        active_request = request

    while not rospy.is_shutdown():
        if request["done"].wait(0.1):
            return request["response"]
    return TriggerResponse(success=False, message="Node is shutting down.")


def main():
    global active_request
    rospy.init_node("auto_move")
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    tf_buffer = tf2_ros.Buffer()
    tf_listener = tf2_ros.TransformListener(tf_buffer)
    rospy.Subscriber("/scan", LaserScan, scan_callback,
                     callback_args=tf_buffer, queue_size=1)
    rospy.Subscriber("/odom", Odometry, odom_callback, queue_size=1)
    service = rospy.Service("/goto_closest", Trigger, goto_closest)
    rospy.on_shutdown(lambda: pub.publish(Twist()))
    rate = rospy.Rate(20)

    while not rospy.is_shutdown():
        with request_lock:
            command = Twist()
            request = active_request
            response = None
            target = goal
            pose = robot_pose
            velocity = robot_velocity
            now = rospy.Time.now()

            if request is not None:
                if (target is None or pose is None or velocity is None
                        or not 0.0 <= (now - target[2]).to_sec() <= SCAN_TIMEOUT):
                    response = TriggerResponse(
                        success=False, message="No valid scan, TF or odometry available.")
                else:
                    dx = target[0] - pose[0]
                    dy = target[1] - pose[1]
                    remaining = math.hypot(dx, dy) - STOP_DISTANCE

                    if remaining > GOAL_TOLERANCE:
                        request["stopped_since"] = None
                        angle_error = math.atan2(dy, dx) - pose[2]
                        angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))
                        command.angular.z = max(
                            -MAX_ANGULAR_SPEED,
                            min(MAX_ANGULAR_SPEED, K_ANGLE * angle_error),
                        )
                        if abs(angle_error) <= math.pi / 4:
                            command.linear.x = min(MAX_LINEAR_SPEED, K_DISTANCE * remaining)
                    elif velocity[0] < 0.01 and velocity[1] < 0.02:
                        if request["stopped_since"] is None:
                            request["stopped_since"] = now
                        if (now - request["stopped_since"]).to_sec() >= STOP_SETTLE_TIME:
                            response = TriggerResponse(
                                success=True, message="Stopped about 0.3 m before the closest object.")
                    else:
                        request["stopped_since"] = None

            pub.publish(command)
            if response is not None:
                active_request = None
                request["response"] = response
                request["done"].set()
        rate.sleep()


if __name__ == "__main__":
    main()
