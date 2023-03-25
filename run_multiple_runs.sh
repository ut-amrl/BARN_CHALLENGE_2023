#!/bin/bash 

currrent_ws=$(dirname $(realpath $0))/..

for j in $(eval echo {$1..$2})
do
    for i in $(eval echo {$3..$4})
    do
        python run.py --algo $5 --param $6 --result_dir "/robodata/smodak/BARN2023/result_$5_$6" --world_idx $i --run_idx $j --gui 0
        pkill -9 python
        pkill -9 rosmaster
        pkill -9 gzclient
        sleep 5s
    done
done
