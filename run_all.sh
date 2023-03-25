#!/bin/bash 

currrent_ws=$(dirname $(realpath $0))/..

for j in {0..25}
do
    for i in {0..299}
    do
        python run_original.py $i $j 0
        pkill -9 python
        pkill -9 rosmaster
        pkill -9 gzclient
        sleep 5s
    done
done
