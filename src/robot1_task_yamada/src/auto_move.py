#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist


def move(x, z, seconds):
    msg = Twist()
    msg.linear.x = x
    msg.angular.z = z

    for i in range(seconds * 10):
        if rospy.is_shutdown():
            break
        pub.publish(msg)
        rate.sleep()

def main():
    global pub, rate

    rospy.init_node("auto_move")
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    rate = rospy.Rate(10)

    while pub.get_num_connections() == 0:
        rospy.sleep(0.1)

    rospy.loginfo("3秒前進")
    move(0.1, 0.0, 3)

    rospy.loginfo("3秒左旋回")
    move(0.0, 0.3, 3)

    rospy.loginfo("2秒前進")
    move(0.1, 0.0, 2)
    
    rospy.loginfo("停止")
    pub.publish(Twist())


if __name__ == "__main__":
    main()
