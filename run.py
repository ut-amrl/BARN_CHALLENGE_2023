import time
import argparse
import subprocess
import os
from os.path import join
import numpy as np
import rospy
import rospkg
import signal
import re
import actionlib
from geometry_msgs.msg import Quaternion
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction

from gazebo_simulation import GazeboSimulation
INIT_POSITION = [-2, 3, 1.57]  # in world frame
GOAL_POSITION = [0, 10]  # 244 278 relative to the initial position


def modify_variables(carrot, fov):
    #  Open the navigation.lua file for reading
    with open("third_party/graph_navigation/config/navigation.lua", "r") as f:
        # Read the contents of the file into a string
        contents = f.read()

    # Define a regular expression pattern to find the value of carrot_dist
    patterns = []
    patterns.append(r"carrot_dist\s*=\s*([\d\.]+)")
    patterns.append(r"local_fov\s*=\sdeg2rad\(([\d\.]+)\)")
    var = [carrot, fov]
    for i, pattern in enumerate(patterns):
        # Find the current value of carrot_dist
        match = re.search(pattern, contents)
        if match:
            current_value = float(match.group(1))
        else:
            # If carrot_dist is not found, set the current value to None
            current_value = None

        # Modify the value of carrot_dist
        new_value = var[i]

        # Replace the current value of carrot_dist with the new value
        if i == 0:
            if current_value is not None:
                contents = re.sub(pattern, f"carrot_dist = {new_value}", contents)
            else:
                # If carrot_dist is not found, add it to the end of the file
                contents += f"\nNavigationParameters.carrot_dist = {new_value};\n"
        else:
            if current_value is not None:
                contents = re.sub(pattern, f"local_fov = deg2rad({new_value})", contents)
            else:
                # If carrot_dist is not found, add it to the end of the file
                contents += f"\nNavigationParameters.local_fov = {new_value};\n"

    # Open the navigation.lua file for writing
    with open("third_party/graph_navigation/config/navigation.lua", "w") as f:
        # Write the modified contents back to the file
        f.write(contents)


def compute_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def path_coord_to_gazebo_coord(x, y):
    RADIUS = 0.075
    r_shift = -RADIUS - (30 * RADIUS * 2)
    c_shift = RADIUS + 5

    gazebo_x = x * (RADIUS * 2) + r_shift
    gazebo_y = y * (RADIUS * 2) + c_shift

    return (gazebo_x, gazebo_y)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='test BARN navigation challenge')
    parser.add_argument('--algo', type=str, help="either mb or vor", default="vor")
    parser.add_argument('--param', type=str, help="either 2022 or 2023", default="2023")
    parser.add_argument('--result_dir', type=str, default='result')
    parser.add_argument('--world_idx', type=int, default=0)
    parser.add_argument('--gui', type=int, default=1)
    parser.add_argument('--run_idx', type=int, default=0)
    parser.add_argument('--out', type=str, default="out.txt")
    args = parser.parse_args()
    # modify_variables(float(sys.argv[3]), int(sys.argv[4]))

    ##########################################################################################
    # 0. Launch Gazebo Simulation
    ##########################################################################################

    os.environ["JACKAL_LASER"] = "1"
    os.environ["JACKAL_LASER_MODEL"] = "ust10"
    os.environ["JACKAL_LASER_OFFSET"] = "-0.065 0 0.01"

    world_name = "BARN/world_%d.world" % (args.world_idx)
    print(">>>>>>>>>>>>>>>>>> Loading Gazebo Simulation with %s <<<<<<<<<<<<<<<<<<" % (world_name))

    rospack = rospkg.RosPack()
    base_path = rospack.get_path('jackal_helper')

    launch_file = join(base_path, 'launch', 'gazebo.launch')
    world_name = join(base_path, "worlds", world_name)

    gazebo_process = subprocess.Popen([
        'roslaunch',
        launch_file,
        'world_name:=' + world_name,
        'gui:=' + ("true" if args.gui == 1 else "false")
    ])
    time.sleep(5)  # sleep to wait until the gazebo being created

    rospy.init_node('gym', anonymous=True)
    rospy.set_param('/use_sim_time', True)

    # GazeboSimulation provides useful interface to communicate with gazebo
    gazebo_sim = GazeboSimulation(init_position=INIT_POSITION)

    init_coor = (INIT_POSITION[0], INIT_POSITION[1])
    goal_coor = (INIT_POSITION[0] + GOAL_POSITION[0], INIT_POSITION[1] + GOAL_POSITION[1])

    pos = gazebo_sim.get_model_state().pose.position
    curr_coor = (pos.x, pos.y)
    collided = True

    # check whether the robot is reset, the collision is False
    while compute_distance(init_coor, curr_coor) > 0.1 or collided:
        gazebo_sim.reset()  # Reset to the initial position
        pos = gazebo_sim.get_model_state().pose.position
        curr_coor = (pos.x, pos.y)
        collided = gazebo_sim.get_hard_collision()
        time.sleep(1)

    ##########################################################################################
    # 1. Launch your navigation stack
    # (Customize this block to add your own navigation stack)
    ##########################################################################################

    if args.algo == "mb":
        # launch move base + graph nav navigation stack
        # is fake DWA with spoofed cmd_vel to cmd_vel_fake
        launch_file = join(base_path, '..', 'jackal_helper/launch/move_base_stack.launch')
        mb_nav_stack_process = subprocess.Popen([
            'roslaunch',
            launch_file,
            'param_value:=' + args.param
        ])

        # Make sure your navigation stack recives a goal of (0, 10, 0), which is 10 meters away
        # along postive y-axis.
        nav_as = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
        mb_goal = MoveBaseGoal()
        mb_goal.target_pose.header.frame_id = 'odom'
        mb_goal.target_pose.pose.position.x = GOAL_POSITION[0]
        mb_goal.target_pose.pose.position.y = GOAL_POSITION[1]
        mb_goal.target_pose.pose.position.z = 0
        mb_goal.target_pose.pose.orientation = Quaternion(0, 0, 0, 1)

        nav_as.wait_for_server()
        nav_as.send_goal(mb_goal)

    elif args.algo == "vor":
        filename = str(args.world_idx)
        record_cmd = 'screencast -s 0.5 {filename}.mp4'
        # launch voronoi + graph nav navigation stack
        # is fake DWA with spoofed cmd_vel to cmd_vel_fake
        launch_file = join(base_path, '..', 'jackal_helper/launch/voronoi_stack.launch')
        mb_nav_stack_process = subprocess.Popen([
            'roslaunch',
            launch_file,
        ])
        proc = subprocess.Popen(record_cmd, shell=True)

    else:
        raise ValueError("Unknown algorithm %s" % (args.algo))

    ##########################################################################################
    # 2. Start navigation
    ##########################################################################################

    curr_time = rospy.get_time()
    pos = gazebo_sim.get_model_state().pose.position
    curr_coor = (pos.x, pos.y)

    # check whether the robot started to move
    while compute_distance(init_coor, curr_coor) < 0.1:
        curr_time = rospy.get_time()
        pos = gazebo_sim.get_model_state().pose.position
        curr_coor = (pos.x, pos.y)
        time.sleep(0.01)

    # start navigation, check position, time and collision
    start_time = curr_time
    start_time_cpu = time.time()
    collided = False

    while curr_coor[1] < 10.1 and not collided and curr_time - start_time < 100:
        curr_time = rospy.get_time()
        pos = gazebo_sim.get_model_state().pose.position
        curr_coor = (pos.x, pos.y)
        print("$$$ Time: %.2f (s), x: %.2f (m), y: %.2f (m)" % (curr_time - start_time, *curr_coor))
        collided = gazebo_sim.get_hard_collision()
        while rospy.get_time() - curr_time < 0.1:
            time.sleep(0.01)

    ##########################################################################################
    # 3. Report metrics and generate log
    ##########################################################################################

    print(">>>>>>>>>>>>>>>>>> Test finished! <<<<<<<<<<<<<<<<<<")
    success = False
    if collided:
        status = "collided"
    elif curr_time - start_time >= 100:
        status = "timeout"
    else:
        status = "succeeded"
        success = True
    print("Navigation %s with time %.4f (s)" % (status, curr_time - start_time))

    path_file_name = join(base_path, "worlds/BARN/path_files", "path_%d.npy" % args.world_idx)
    path_array = np.load(path_file_name)
    path_array = [path_coord_to_gazebo_coord(*p) for p in path_array]
    path_array = np.insert(path_array, 0, (INIT_POSITION[0], INIT_POSITION[1]), axis=0)
    path_array = np.insert(path_array, len(path_array), (INIT_POSITION[0] + GOAL_POSITION[0], INIT_POSITION[1] + GOAL_POSITION[1]), axis=0)
    path_length = 0
    for p1, p2 in zip(path_array[:-1], path_array[1:]):
        path_length += compute_distance(p1, p2)

    # Navigation metric: 1_success *  optimal_time / clip(actual_time, 4 * optimal_time, 8 * optimal_time)
    optimal_time = path_length / 2
    actual_time = curr_time - start_time
    nav_metric = int(success) * optimal_time / np.clip(actual_time, 4 * optimal_time, 8 * optimal_time)
    print("Navigation metric: %.4f" % (nav_metric))

    isExist = os.path.exists(f"{args.result_dir}/")

    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(f"{args.result_dir}/")
    with open("{}/run_{}.log".format(args.result_dir, args.run_idx), 'a') as f:
        result = [args.world_idx, status, curr_time - start_time, nav_metric]
        f.write(f"{result}\n")

    # with open(args.out, "wb") as f:
    #     f.write("%d %d %d %d %.4f %.4f\n".encode() %(args.world_idx, success, collided, (curr_time - start_time)>=100, curr_time - start_time, nav_metric))
    # Wait for the recording to finish
    proc.wait()
    os.system('rosnode kill collision_pub_gazebo')
    mb_nav_stack_process.send_signal(signal.SIGINT)
    gazebo_process.send_signal(signal.SIGINT)
    print('finish cleanly')

    time.sleep(10)
    os.system('killall -9 gazebo; killall -9 gzserver; killall -9 gzclient; killall -9 rosmaster; killall -9 roscore; killall -9 python')
    time.sleep(10)
