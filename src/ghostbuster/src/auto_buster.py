#!/usr/bin/env python3
import math
import rospy
from geometry_msgs.msg import PolygonStamped, PoseStamped
from nav_msgs.msg import Odometry
from std_srvs.srv import Empty


CATCH_DISTANCE = 0.45
GOAL_TIMEOUT = rospy.Duration(45)
GOAL_RESEND_INTERVAL = rospy.Duration(2)
RETRY_DELAY = rospy.Duration(12)
APPROACH_RADIUS = 0.28


class AutoBuster:
    def __init__(self):
        self.ghosts = frozenset()
        self.position = None
        self.target = None
        self.deadline = None
        self.goal = None
        self.last_goal_sent = None
        self.accepted_goal = None
        self.retry_at = {}
        self.attempts = {}
        self.goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)
        self.accepted_goal_sub = rospy.Subscriber(
            '/move_base/current_goal', PoseStamped, self.update_accepted_goal, queue_size=1
        )
        self.buster = rospy.ServiceProxy('/buster', Empty)
        self.ghost_sub = rospy.Subscriber('/ghost', PolygonStamped, self.update_ghosts, queue_size=1)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.update_position, queue_size=1)

    def update_ghosts(self, message):
        self.ghosts = frozenset(
            (message.header.frame_id, p.x, p.y) for p in message.polygon.points
        )

    def update_position(self, message):
        position = message.pose.pose.position
        self.position = (position.x, position.y)

    def update_accepted_goal(self, message):
        self.accepted_goal = (message.header.frame_id, message.pose.position.x, message.pose.position.y)

    def send_goal(self, ghost, position, now):
        frame, x, y = ghost
        attempt = self.attempts.get(ghost, 0) % 9
        if attempt == 0:
            goal_x, goal_y = x, y
            yaw = math.atan2(y - position[1], x - position[0])
        else:
            angle = (attempt - 1) * math.pi / 4
            goal_x = x + APPROACH_RADIUS * math.cos(angle)
            goal_y = y + APPROACH_RADIUS * math.sin(angle)
            yaw = math.atan2(y - goal_y, x - goal_x)

        goal = PoseStamped()
        goal.header.frame_id = frame
        goal.pose.position.x = goal_x
        goal.pose.position.y = goal_y
        goal.pose.orientation.z = math.sin(yaw / 2)
        goal.pose.orientation.w = math.cos(yaw / 2)
        self.goal = goal
        self.accepted_goal = None
        self.publish_goal(now)
        self.target = ghost
        self.deadline = now + GOAL_TIMEOUT
        rospy.loginfo('Chasing ghost at (%.2f, %.2f)', x, y)

    def publish_goal(self, now):
        self.goal.header.stamp = now
        self.goal_pub.publish(self.goal)
        self.last_goal_sent = now

    def catch(self, ghost, now):
        if self.target == ghost:
            self.target = None
        self.retry_at[ghost] = now + rospy.Duration(2)
        try:
            self.buster()
        except rospy.ServiceException as error:
            rospy.logwarn_throttle(5, 'Calling /buster failed: %s', error)

    def step(self, now):
        ghosts, position = self.ghosts, self.position
        for history in (self.retry_at, self.attempts):
            for ghost in history.keys() - ghosts:
                del history[ghost]

        if self.target is not None and self.target not in ghosts:
            self.target = None
        if not ghosts or position is None:
            return

        def distance(ghost):
            return math.hypot(ghost[1] - position[0], ghost[2] - position[1])

        ready = ghosts - {ghost for ghost, retry in self.retry_at.items() if now < retry}
        nearest = min(ready, key=distance, default=None)
        if nearest is not None and distance(nearest) < CATCH_DISTANCE:
            self.catch(nearest, now)
            return

        if self.target is not None:
            if now < self.deadline:
                goal = self.goal
                expected = (goal.header.frame_id, goal.pose.position.x, goal.pose.position.y)
                if self.accepted_goal != expected and now - self.last_goal_sent >= GOAL_RESEND_INTERVAL:
                    self.publish_goal(now)
                return
            ghost = self.target
            self.target = None
            self.attempts[ghost] = self.attempts.get(ghost, 0) + 1
            self.retry_at[ghost] = now + RETRY_DELAY
            rospy.logwarn('Could not get within catching range of (%.2f, %.2f); will retry', *ghost[1:])
            return

        if nearest is not None and self.goal_pub.get_num_connections():
            self.send_goal(nearest, position, now)

    def run(self):
        rospy.loginfo('Waiting for /move_base and /buster')
        rospy.wait_for_service('/buster')
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.step(rospy.Time.now())
            rate.sleep()


if __name__ == '__main__':
    rospy.init_node('auto_buster')
    try:
        AutoBuster().run()
    except rospy.ROSInterruptException:
        pass
