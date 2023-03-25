#!/bin/bash 

cd jackal_helper/script
chmod +x *.sh
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

cd ../../..
catkin_make