#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry


def callback(message):
    position = message.pose.pose.position
    rospy.loginfo("x = %.4f m, y = %.4f m", position.x, position.y)


def main():
    rospy.init_node("odom_listener")
    rospy.Subscriber("/odom", Odometry, callback)
    rospy.spin()  # メッセージの受信を続けます。


if __name__ == "__main__":
    main()
