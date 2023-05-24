import time
import subprocess
import os
from os.path import join
import sys
import numpy as np
import rospy
import rospkg
import roslib 
roslib.load_manifest("amrl_msgs")
import signal
import re
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from amrl_msgs.msg import Localization2DMsg
import actionlib
from geometry_msgs.msg import Quaternion

if __name__ == "__main__":
    os.environ["JACKAL_LASER"] = "1"
    os.environ["JACKAL_LASER_MODEL"] = "ust10"
    os.environ["JACKAL_LASER_OFFSET"] = "-0.065 0 0.01"

    rospack = rospkg.RosPack()
    base_path = rospack.get_path('jackal_helper')

    launch_file = join(base_path, '..', 'jackal_helper/launch/voronoi_stack.launch')
    mb_nav_stack_process = subprocess.Popen([
        'roslaunch',
        launch_file,
    ])

    while True:
        rospy.spin()