#!/bin/bash 

currrent_ws=$(dirname $(realpath $0))/..

for j in {0..1}
do
    for i in {275..299}
    do
        python run_original.py $i $j
        pkill -9 python
        pkill -9 rosmaster
        pkill -9 gzclient
        sleep 5s
    done
done
