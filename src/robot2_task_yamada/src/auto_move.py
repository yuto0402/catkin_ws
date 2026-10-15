#!/usr/bin/env python3
import math

import rospy
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion

goal = None
robot_pose = None

K_ANGLE = 1.0
K_DISTANCE = 0.5
MAX_LINEAR_SPEED = 0.25
MAX_ANGULAR_SPEED = 0.5
GOAL_TOLERANCE = 0.05

def callback(message):
    global goal
    goal = (message.pose.position.x, message.pose.position.y)


def odom_callback(message):
    global robot_pose
    position = message.pose.pose.position
    q = message.pose.pose.orientation
    _, _, yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])
    robot_pose = (position.x, position.y, yaw)


def main():
    rospy.init_node("auto_move")
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    rospy.Subscriber("/move_base_simple/goal", PoseStamped, callback, queue_size=1)
    rospy.Subscriber("/odom", Odometry, odom_callback, queue_size=1)
    rate = rospy.Rate(20)

    while not rospy.is_shutdown():
        command = Twist()
        target = goal
        pose = robot_pose

        if target is not None and pose is not None:
            dx = target[0] - pose[0]
            dy = target[1] - pose[1]
            distance = math.hypot(dx, dy)

            if distance > GOAL_TOLERANCE:
                angle_error = math.atan2(dy, dx) - pose[2]
                angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))
                command.angular.z = max(
                    -MAX_ANGULAR_SPEED,
                    min(MAX_ANGULAR_SPEED, K_ANGLE * angle_error),
                )

                if abs(angle_error) <= math.pi / 4:
                    command.linear.x = min(MAX_LINEAR_SPEED, K_DISTANCE * distance)

        pub.publish(command)
        rate.sleep()


if __name__ == "__main__":
    main()
