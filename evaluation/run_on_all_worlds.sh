#!/bin/bash

for world_idx in {0..299}
do
    python3 run.py --world_idx $world_idx --run_idx 3
    pkill -9 python
    pkill -9 rosmaster
    pkill -9 gzclient
    sleep 5s
done