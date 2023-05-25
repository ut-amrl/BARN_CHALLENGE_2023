#!/bin/bash 

cd src/jackal_helper/script
chmod +x *.sh
find . -name "*.py" -exec chmod +x {} \;
cd -

git submodule update --recursive --init
# export ROS_PACKAGE_PATH=`pwd`:$ROS_PACKAGE_PATH

cd third_party/amrl_msgs
make -j12 

cd ../enml
git checkout icra_2023_barn_challenge
make -j12

cd ../graph_navigation
git checkout icra_2023_barn_challenge
mkdir build
cd build 
cmake ..
make -j12

cd ../../webviz
git checkout icra_2023_barn_challenge
mkdir build
cd build 
cmake ..
make -j12

cd ../../voronoi_global_planner
git checkout main

# cd ../../..
# catkin_make
