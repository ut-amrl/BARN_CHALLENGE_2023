#!/bin/bash 

ut_jackal_path=$(realpath third_party/ut_jackal)
echo $ut_jackal_path
graph_nav_path=$(realpath third_party/ut_jackal/graph_navigation)
echo $graph_nav_path
amrl_msgs_path=$(realpath third_party/amrl_msgs)
echo $amrl_msgs_path

if [[ $ROS_PACKAGE_PATH == *"ut_jackal"* ]]; then
    echo "Removing ut_jackal from ROS_PACKAGE_PATH..."
    export ROS_PACKAGE_PATH=$(echo $ROS_PACKAGE_PATH | tr ':' '\n' | grep -v "ut_jackal" | paste -sd: -)
fi
# Add the new path to ROS_PACKAGE_PATH
if [[ $ROS_PACKAGE_PATH != *"$ut_jackal_path"* ]]; then
    echo "Adding $ut_jackal_path to ROS_PACKAGE_PATH..."
    export ROS_PACKAGE_PATH=$ut_jackal_path:$ROS_PACKAGE_PATH
fi

if [[ $ROS_PACKAGE_PATH == *"graph_navigation"* ]]; then
    echo "Removing graph_navigation from ROS_PACKAGE_PATH..."
    export ROS_PACKAGE_PATH=$(echo $ROS_PACKAGE_PATH | tr ':' '\n' | grep -v "graph_navigation" | paste -sd: -)
fi
# Add the new path to ROS_PACKAGE_PATH
if [[ $ROS_PACKAGE_PATH != *"$graph_nav_path"* ]]; then
    echo "Adding $graph_nav_path to ROS_PACKAGE_PATH..."
    export ROS_PACKAGE_PATH=$graph_nav_path:$ROS_PACKAGE_PATH
fi

if [[ $ROS_PACKAGE_PATH == *"amrl_msgs"* ]]; then
    echo "Removing amrl_msgs from ROS_PACKAGE_PATH..."
    export ROS_PACKAGE_PATH=$(echo $ROS_PACKAGE_PATH | tr ':' '\n' | grep -v "amrl_msgs" | paste -sd: -)
fi
# Add the new path to ROS_PACKAGE_PATH
if [[ $ROS_PACKAGE_PATH != *"$amrl_msgs_path"* ]]; then
    echo "Adding $amrl_msgs_path to ROS_PACKAGE_PATH..."
    export ROS_PACKAGE_PATH=$amrl_msgs_path:$ROS_PACKAGE_PATH
fi

cd src/jackal_helper/script
chmod +x *.sh
find . -name "*.py" -exec chmod +x {} \;
cd -

git submodule update --recursive --init
# export ROS_PACKAGE_PATH=`pwd`:$ROS_PACKAGE_PATH

cd third_party/amrl_msgs
make -j12 

cd ../ut_jackal
make -j12

cd ../voronoi_global_planner
git checkout main

cd ../..
catkin_make
