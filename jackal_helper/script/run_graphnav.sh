#!/bin/bash

echo $(dirname $(realpath $0))
cd $(dirname $(realpath $0))

cd ../../third_party/graph_navigation
echo `pwd`

./bin/navigation --dw 10.0 --cw 0.2 --fw 0.1 move_base_simple/goal:=move_base_simple/localgoal