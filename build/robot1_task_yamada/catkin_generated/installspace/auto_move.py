#!/usr/bin/env python3
import time

import rospy
from geometry_msgs.msg import Twist


def move(publisher, linear_x, angular_z, duration):
    command = Twist()  # 指定しない成分はすべて 0 です。
    command.linear.x = linear_x
    command.angular.z = angular_z
    end_time = rospy.Time.now() + rospy.Duration(duration)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown() and rospy.Time.now() < end_time:
        publisher.publish(command)
        rate.sleep()


def main():
    rospy.init_node("auto_move")
    publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

    def stop():
        # 最後の速度指令が残らないよう、停止指令を繰り返し送ります。
        for _ in range(3):
            publisher.publish(Twist())
            time.sleep(0.05)

    rospy.on_shutdown(stop)
    try:
        # Gazebo との接続が完了してから動き始めます。
        deadline = time.monotonic() + 5.0
        while publisher.get_num_connections() == 0 and not rospy.is_shutdown():
            if time.monotonic() >= deadline:
                rospy.logerr("/cmd_vel の受信ノードがありません。Gazebo を起動してください。")
                return
            time.sleep(0.1)
        if rospy.is_shutdown():
            return
        rospy.sleep(0.1)  # シミュレーション時刻の受信を待ちます。

        rospy.loginfo("前進：0.1 m/s、3秒")
        move(publisher, 0.1, 0.0, 3.0)
        if rospy.is_shutdown():
            return
        rospy.loginfo("左旋回：0.3 rad/s、3秒")
        move(publisher, 0.0, 0.3, 3.0)
        if rospy.is_shutdown():
            return
        rospy.loginfo("前進：0.1 m/s、2秒")
        move(publisher, 0.1, 0.0, 2.0)
        rospy.loginfo("停止")
    except rospy.ROSInterruptException:
        pass
    finally:
        stop()


if __name__ == "__main__":
    main()
