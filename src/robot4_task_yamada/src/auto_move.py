#!/usr/bin/env python3
import math

import cv2
import rospy
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image
from std_srvs.srv import Empty


FOCAL = 265.23
CENTER = 160.5
bridge = CvBridge()
observation = None
robot_pose = None


def detect_ball(image, min_area=8.0):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0, 100, 45), (10, 255, 255))
    mask |= cv2.inRange(hsv, (170, 100, 45), (179, 255, 255))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = [c for c in contours if cv2.contourArea(c) >= min_area]
    if not candidates:
        return None
    contour = max(candidates, key=cv2.contourArea)
    moments = cv2.moments(contour)
    if moments['m00'] == 0:
        return None
    _, radius = cv2.minEnclosingCircle(contour)
    return (moments['m10'] / moments['m00'],
            moments['m01'] / moments['m00'], radius)


def approach_velocity(bearing, max_linear, max_angular, gain, distance=None):
    angular = max(-max_angular, min(max_angular, gain * bearing))
    if abs(bearing) >= 0.6:
        linear = 0.0
    else:
        linear = max_linear * max(0.0, math.cos(bearing))
        if distance is not None and abs(bearing) > 0.05:
            turn_limit = abs(angular) * max(distance, 0.0) / (2 * abs(math.sin(bearing)))
            linear = min(linear, turn_limit)
    return linear, angular


def search_velocity(pose, elapsed, direction, max_linear, max_angular):
    scan_duration = 2 * math.pi / max(max_angular, 0.01)
    if elapsed < scan_duration or pose is None:
        return 0.0, direction * max_angular, False
    if math.hypot(pose[0], pose[1]) <= 0.8:
        return 0.0, direction * max_angular, True
    bearing = center_bearing(pose)
    linear, angular = approach_velocity(bearing, max_linear, max_angular, 3.5)
    return linear, angular, False


def center_bearing(pose):
    x, y, yaw = pose
    angle = math.atan2(-y, -x) - yaw
    return math.atan2(math.sin(angle), math.cos(angle))


def image_callback(message):
    global observation
    try:
        image = bridge.imgmsg_to_cv2(message, 'bgr8')
        observation = (message.header.stamp, detect_ball(image))
    except (CvBridgeError, cv2.error) as error:
        observation = None
        rospy.logwarn_throttle(5, 'Cannot process image: %s', error)


def odom_callback(message):
    global robot_pose
    p = message.pose.pose.position
    q = message.pose.pose.orientation
    yaw = math.atan2(2 * (q.w * q.z + q.x * q.y),
                     1 - 2 * (q.y * q.y + q.z * q.z))
    robot_pose = (p.x, p.y, yaw, message.header.stamp)


def main():
    rospy.init_node('ball_collector')
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    rospy.Subscriber('camera/image', Image, image_callback, queue_size=1, buff_size=2**20)
    rospy.Subscriber('odom', Odometry, odom_callback, queue_size=1)
    rospy.on_shutdown(lambda: pub.publish(Twist()))
    rate = rospy.Rate(30)

    if rospy.get_param('~auto_start', False):
        rospy.wait_for_service('/start_game', timeout=60)
        while observation is None and not rospy.is_shutdown():
            rate.sleep()
        if rospy.is_shutdown():
            return
        rospy.sleep(1)
        rospy.ServiceProxy('/start_game', Empty)()
        rospy.sleep(1.05)

    direction = 1.0
    search_start = None
    last_score = rospy.get_param('score', 0)
    next_score_check = rospy.Time.now()
    captured = False

    while not rospy.is_shutdown():
        now = rospy.Time.now()
        image, pose = observation, robot_pose
        command = Twist()

        if now >= next_score_check:
            score = rospy.get_param('score', 0)
            captured = captured or score > last_score
            last_score = score
            next_score_check = now + rospy.Duration(0.2)

        if image is not None and 0 <= (now - image[0]).to_sec() <= 0.5:
            ball = image[1]
            if ball is not None:
                search_start = None
                captured = False
                u, _, radius = ball
                bearing = math.atan2(CENTER - u, FOCAL)
                if abs(bearing) > 0.05:
                    direction = math.copysign(1, bearing)
                distance = 0.15 * FOCAL / max(radius, 1)
                command.linear.x, command.angular.z = approach_velocity(
                    bearing, 0.25, 0.5, 3.5, distance)
            else:
                if pose is not None and not 0 <= (now - pose[3]).to_sec() <= 0.5:
                    pose = None
                if search_start is None or now < search_start:
                    search_start = now
                if captured and pose is not None:
                    inward = center_bearing(pose[:3])
                    if abs(inward) > 0.05:
                        direction = math.copysign(1, inward)
                    search_start = now
                    captured = False
                elapsed = (now - search_start).to_sec()
                command.linear.x, command.angular.z, reset = search_velocity(
                    pose[:3] if pose is not None else None, elapsed, direction, 0.25, 0.5)
                if reset:
                    search_start = now
        else:
            search_start = None

        pub.publish(command)
        rate.sleep()


if __name__ == '__main__':
    try:
        main()
    except (rospy.ROSInterruptException, rospy.ROSException, rospy.ServiceException) as error:
        if not rospy.is_shutdown():
            rospy.logerr('Ball collector stopped: %s', error)
