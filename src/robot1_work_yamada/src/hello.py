#!/usr/bin/env python3
import rospy

def hello():
    # ROSノードの初期化
    rospy.init_node('hello_ros')

    # ログメッセージを出力
    rospy.loginfo("Hello, ROS!")

# 上の関数を実行する
hello()
