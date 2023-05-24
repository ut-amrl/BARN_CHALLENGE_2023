#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
import math
import sys
global localG
global odom
global PARAM



def callback(data):
    global localG
    global pose_pub
    global PARAM
    global odom
    localgoal = data.poses[-1]
    localG = localgoal
    if(odom == None):
        return
    posx = odom.pose.pose.position.x
    posy = odom.pose.pose.position.y
    diffx = odom.pose.pose.position.x - data.poses[0].pose.position.x
    diffy = odom.pose.pose.position.y - data.poses[0].pose.position.y
<<<<<<< HEAD:src/jackal_helper/script/localgoal_2023.py
    goals = []
=======
>>>>>>> zichao:src/jackal_helper/script/2022_challenge/localgoal_2022.py

    for possibleGoal in data.poses:
        possibleGoal.pose.position.x = possibleGoal.pose.position.x + diffx
        possibleGoal.pose.position.y = possibleGoal.pose.position.y + diffy
        goalx = possibleGoal.pose.position.x
        goaly = possibleGoal.pose.position.y

        # Calculate distance between current position and goal
        dist = math.sqrt((posx - goalx)**2 + (posy - goaly)**2)

<<<<<<< HEAD:src/jackal_helper/script/localgoal_2023.py
        # If the distance is greater than 0.3, publish the goal
        if((PARAM == "2022" and dist < 1 and dist > 0.75) or (PARAM == "2023" and dist > 0.3)):
=======
        if(dist < 1 and dist > 0.75):
>>>>>>> zichao:src/jackal_helper/script/2022_challenge/localgoal_2022.py
            pose_pub.publish(possibleGoal)
            return


def callbackO(data):
    global odom
    odom = data


def main():
    global PARAM
    PARAM = sys.argv[1]
    global pose_pub
    global localG
    localG = None
    global odom
    odom = None
    rospy.init_node('listen', anonymous=True)
    pose_pub = rospy.Publisher("move_base_simple/localgoal", PoseStamped, queue_size=1)
<<<<<<< HEAD:src/jackal_helper/script/localgoal_2023.py
    rospy.Subscriber("/PathTopic", Path, callback)
=======
    rospy.Subscriber("/move_base/TrajectoryPlannerROS/global_plan", Path, callback)
>>>>>>> zichao:src/jackal_helper/script/2022_challenge/localgoal_2022.py

    rospy.Subscriber("enml_odometry", Odometry, callbackO)

    rospy.spin()


if __name__ == '__main__':
    main()
