#!/bin/bash 

git submodule update --recursive --init
export ROS_PACKAGE_PATH=`pwd`:$ROS_PACKAGE_PATH

cd third_party/amrl_msgs
make -j12 

cd ../enml
git checkout icra_2023_barn_challenge
make -j12

sudo apt install libgoogle-glog-dev libgflags-dev liblua5.1-0-dev
cd ../graph_navigation
mkdir build
cd build 
cmake ..
make -j12