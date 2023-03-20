#!/bin/bash

for world_idx in {41..299}
do
    python3 run_voronoi.py $world_idx 2 1 60
    pkill -9 python
    pkill -9 rosmaster
    pkill -9 gzclient
    sleep 5s
done