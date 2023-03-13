#!/bin/bash 

currrent_ws=$(dirname $(realpath $0))/..

for j in {5..49}
do
    for i in {0..299}
    do
        python run.py $i $j
        pkill -9 python
        pkill -9 rosmaster
        pkill -9 gzclient
        sleep 5s
    done
done
