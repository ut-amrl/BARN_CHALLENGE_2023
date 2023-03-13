#!/bin/bash
echo $(dirname $(realpath $0))
cd $(dirname $(realpath $0))
./bin/navigation --dw 10.0 --cw 0.2 --fw 0.1 move_base_simple/goal:=move_base_simple/localgoal