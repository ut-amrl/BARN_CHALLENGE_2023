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
    distances = [] # list of distances from each point within radius to line
    points = [] # create a numpy array with the same length as data.poses



    # find the first pose greater than 1m away
    for i in len(data.poses):
        possibleGoal = data.poses[i]
        goalx = possibleGoal.pose.position.x
        goaly = possibleGoal.pose.position.y
        points.append([goalx, goaly])
        dist = math.sqrt((posx - goalx)**2 + (posy - goaly)**2)
        if(dist > 1):
            break

    points = np.array(points)
    p1 = points[0]
    p2 = points[-1]
    for pt in points.shape[0]:
        d = np.cross(p2-p1, p1-pt)/np.linalg.norm(p2-p1)
        distances.append(d)

    distances = np.array(distances)
    if (np.sum(distances)<0.3): # change this later
        return data.poses[len(points)-1]
    
    # return pose with max distance
    return data.poses[np.argmax(distances)]


        


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