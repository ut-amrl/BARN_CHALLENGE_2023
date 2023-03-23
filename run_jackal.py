import time
import subprocess
import os
from os.path import join
import sys
import numpy as np
import rospy
import rospkg
import signal
import re
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from amrl_msgs.msg import Localization2DMsg
import actionlib
from geometry_msgs.msg import Quaternion
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction

INIT_POSITION = [0, 0]  # in world frame
GOAL_POSITION = [0, 0]  # 244 278 relative to the initial position


class NavGoalListener:
    def __init__(self):
        self.loc_x = 0
        self.loc_y = 0
        rospy.Subscriber("/initialpose", PoseWithCovarianceStamped, self.init_callback, queue_size=1)
        rospy.Subscriber("/move_base_simple/goal", PoseStamped, self.goal_callback, queue_size=1)
        rospy.Subscriber("/localization", Localization2DMsg, self.loc_callback, queue_size=1)

    def init_callback(self, msg):
        global INIT_POSITION
        INIT_POSITION[0] = msg.pose.pose.position.x
        INIT_POSITION[1] = msg.pose.pose.position.y

    def goal_callback(self, msg):
        global GOAL_POSITION
        GOAL_POSITION[0] = msg.pose.position.x - INIT_POSITION[0]
        GOAL_POSITION[1] = msg.pose.position.y - INIT_POSITION[1]

    def loc_callback(self, msg):
        self.loc_x = msg.pose.x
        self.loc_y = msg.pose.y


def compute_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


if __name__ == "__main__":
    rospy.init_node('run_jackal', anonymous=False)
    n = NavGoalListener()
    time.sleep(2)
    init_coor = (INIT_POSITION[0], INIT_POSITION[1])
    goal_coor = (INIT_POSITION[0] + GOAL_POSITION[0], INIT_POSITION[1] + GOAL_POSITION[1])

    curr_coor = (n.loc_x, n.loc_y)

    rospack = rospkg.RosPack()
    base_path = rospack.get_path('jackal_helper')
    launch_file = join(base_path, '..', 'jackal_helper/launch/move_base_DWA.launch')
    mb_nav_stack_process = subprocess.Popen([
        'roslaunch',
        launch_file,
    ])

    print("Set init and goal. Sleeping for 3 min.")
    time.sleep(180)
    print("Awake")

    nav_as = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
    mb_goal = MoveBaseGoal()
    mb_goal.target_pose.header.frame_id = 'odom'
    mb_goal.target_pose.pose.position.x = GOAL_POSITION[0]
    mb_goal.target_pose.pose.position.y = GOAL_POSITION[1]
    mb_goal.target_pose.pose.position.z = 0
    mb_goal.target_pose.pose.orientation = Quaternion(0, 0, 0, 1)

    nav_as.wait_for_server()
    nav_as.send_goal(mb_goal)

    curr_time = rospy.get_time()

    start_time = curr_time
    start_time_cpu = time.time()

    while curr_coor[1] < GOAL_POSITION[1] + 0.5 and curr_time - start_time < 100:
        curr_time = rospy.get_time()
        curr_coor = (n.loc_x, n.loc_y)
        print("$$$ Time: %.2f (s), x: %.2f (m), y: %.2f (m)" % (curr_time - start_time, *curr_coor))
        while rospy.get_time() - curr_time < 0.1:
            time.sleep(0.01)

    success = False
    if curr_time - start_time >= 100:
        status = "timeout"
    else:
        status = "succeeded"
        success = True
    print("Navigation %s with time %.4f (s)" % (status, curr_time - start_time))

    mb_nav_stack_process.send_signal(signal.SIGINT)
    print('finish cleanly')
    time.sleep(10)
