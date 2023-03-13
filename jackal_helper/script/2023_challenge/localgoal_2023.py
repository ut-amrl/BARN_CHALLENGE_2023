#!/usr/bin/env python
import os
import rospy
from actionlib_msgs.msg import GoalStatus
import subprocess
import time
import signal
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from nav_msgs.msg import Odometry

import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import String
import dynamic_reconfigure.client
import math
global localG
global odom
import numpy as np
# def find_the_closest_free_vertex(paths):
#     for path in paths:


def callback(data):
    global localG
    global pose_pub
    global odom
    localgoal = data.poses[-1]
    localG = localgoal
    if(odom == None):
        return
    posx = odom.pose.pose.position.x
    posy = odom.pose.pose.position.y
    diffx = odom.pose.pose.position.x - data.poses[0].pose.position.x
    diffy = odom.pose.pose.position.y - data.poses[0].pose.position.y
    goals = []

    # check first goal is close enough 

    # draw line between two points
    for possibleGoal in data.poses:
        possibleGoal.pose.position.x = possibleGoal.pose.position.x + diffx
        possibleGoal.pose.position.y = possibleGoal.pose.position.y + diffy
        goalx = possibleGoal.pose.position.x
        goaly = possibleGoal.pose.position.y

        # angle = np.arctan2(goaly, goalx)
        # print(angle)
        # if angle > np.pi / 15:

        #     pose_pub.publish(goals[-1])
        #     return
        # goals.append(possibleGoal)

        dist = math.sqrt((posx - goalx)**2 + (posy - goaly)**2)
        if(dist > 0.3):
            pose_pub.publish(possibleGoal)
            return

def callbackO(data):
    global odom
    odom = data

def main():
    global pose_pub
    global localG 
    localG = None
    global odom 
    odom = None
    rospy.init_node('listen',anonymous=True)
    pose_pub = rospy.Publisher("move_base_simple/localgoal",PoseStamped,queue_size=1)
    rospy.Subscriber("/luisa_path", Path, callback)
    
    rospy.Subscriber("enml_odometry", Odometry, callbackO)

    rospy.spin()

if __name__ == '__main__':
    main()