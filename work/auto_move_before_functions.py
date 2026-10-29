#!/usr/bin/env python3
import math
import threading

import cv2
import numpy as np
import rospy
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import CameraInfo, Image
from std_srvs.srv import Empty


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
    """Scan once, then move inward to change the viewpoint if still empty."""
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


class BallCollector:
    def __init__(self):
        self.bridge = CvBridge()
        self.lock = threading.Lock()
        self.observation = None
        self.camera = None
        self.pose = None
        self.max_linear = min(0.25, max(0.0, rospy.get_param('~max_linear_speed', 0.25)))
        self.max_angular = min(0.5, max(0.0, rospy.get_param('~max_angular_speed', 0.5)))
        self.gain = rospy.get_param('~steering_gain', 3.5)
        self.min_area = rospy.get_param('~min_ball_area', 8.0)
        self.image_timeout = rospy.get_param('~image_timeout', 0.5)
        self.search_direction = 1.0
        self.mode = None
        self.search_since = None
        self.score = None
        self.score_poll_at = None
        self.pending_capture_search = False
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.debug_pub = rospy.Publisher('ball_collector/debug_image', Image, queue_size=1)
        self.info_sub = rospy.Subscriber('camera/camera_info', CameraInfo,
                                         self.camera_callback, queue_size=1)
        self.image_sub = rospy.Subscriber('camera/image', Image, self.image_callback,
                                          queue_size=1, buff_size=2**20)
        self.odom_sub = rospy.Subscriber('odom', Odometry, self.odom_callback, queue_size=1)
        rospy.on_shutdown(self.stop)

    def camera_callback(self, message):
        if message.K[0] > 0:
            with self.lock:
                self.camera = (message.K[0], message.K[2])

    def odom_callback(self, message):
        p = message.pose.pose.position
        q = message.pose.pose.orientation
        yaw = math.atan2(2 * (q.w * q.z + q.x * q.y),
                         1 - 2 * (q.y * q.y + q.z * q.z))
        with self.lock:
            self.pose = (p.x, p.y, yaw, message.header.stamp)

    def image_callback(self, message):
        try:
            image = self.bridge.imgmsg_to_cv2(message, desired_encoding='bgr8')
            detection = detect_ball(image, self.min_area)
        except (CvBridgeError, cv2.error) as error:
            rospy.logwarn_throttle(5.0, 'Cannot process camera image: %s', error)
            with self.lock:
                self.observation = None
            return
        with self.lock:
            self.observation = (message.header.stamp, detection)
        if self.debug_pub.get_num_connections():
            debug = image.copy()
            if detection is not None:
                u, v, radius = detection
                cv2.circle(debug, (round(u), round(v)), round(radius), (0, 255, 0), 2)
            annotated = self.bridge.cv2_to_imgmsg(debug, encoding='bgr8')
            annotated.header = message.header
            self.debug_pub.publish(annotated)

    def stop(self):
        self.pub.publish(Twist())

    def run(self):
        if rospy.get_param('~auto_start', False):
            rospy.loginfo('Waiting for the camera and /start_game...')
            rospy.wait_for_service('/start_game', timeout=60.0)
            wait_rate = rospy.Rate(20)
            while not rospy.is_shutdown():
                with self.lock:
                    ready = self.observation is not None and self.camera is not None
                if ready:
                    break
                wait_rate.sleep()
            if rospy.is_shutdown():
                return
            rospy.sleep(1.0)
            rospy.ServiceProxy('/start_game', Empty)()
            rospy.sleep(1.05)
            rospy.loginfo('Ball collection started (camera detection, odometry-guided search).')

        rate = rospy.Rate(30)
        while not rospy.is_shutdown():
            with self.lock:
                observation, camera, pose = self.observation, self.camera, self.pose
            now = rospy.Time.now()
            if self.score_poll_at is None or now >= self.score_poll_at:
                score = rospy.get_param('score', 0)
                if self.score is not None and score > self.score:
                    self.pending_capture_search = True
                self.score = score
                self.score_poll_at = now + rospy.Duration(0.2)
            command = Twist()
            mode = 'WAIT_CAMERA'
            if observation is not None and camera is not None:
                stamp, detection = observation
                age = (rospy.Time.now() - stamp).to_sec()
                if 0.0 <= age <= self.image_timeout:
                    if detection is None:
                        mode = 'SEARCH'
                        pose_fresh = (pose is not None and
                                      0 <= (rospy.Time.now() - pose[3]).to_sec() <= 0.5)
                        now = rospy.Time.now()
                        if self.mode != 'SEARCH' or self.search_since is None:
                            self.search_since = now
                        if self.pending_capture_search and pose_fresh:
                            inward = center_bearing(pose[:3])
                            if abs(inward) > 0.05:
                                self.search_direction = math.copysign(1.0, inward)
                            self.search_since = now
                            self.pending_capture_search = False
                        elapsed = (now - self.search_since).to_sec()
                        if elapsed < 0:
                            self.search_since = now
                            elapsed = 0.0
                        command.linear.x, command.angular.z, reset = search_velocity(
                            pose[:3] if pose_fresh else None, elapsed,
                            self.search_direction, self.max_linear, self.max_angular)
                        if reset:
                            self.search_since = now
                    else:
                        mode = 'APPROACH'
                        self.pending_capture_search = False
                        focal_length, center = camera
                        bearing = math.atan2(center - detection[0], focal_length)
                        if abs(bearing) > 0.05:
                            self.search_direction = math.copysign(1.0, bearing)
                        command.linear.x, command.angular.z = approach_velocity(
                            bearing, self.max_linear, self.max_angular, self.gain,
                            distance=0.15 * focal_length / max(detection[2], 1.0))
            if mode != self.mode:
                rospy.loginfo('Ball collector: %s', mode)
                self.mode = mode
            self.pub.publish(command)
            rate.sleep()


if __name__ == '__main__':
    rospy.init_node('ball_collector')
    try:
        BallCollector().run()
    except (rospy.ROSInterruptException, rospy.ROSException, rospy.ServiceException) as error:
        if not rospy.is_shutdown():
            rospy.logerr('Ball collector stopped: %s', error)
            raise
