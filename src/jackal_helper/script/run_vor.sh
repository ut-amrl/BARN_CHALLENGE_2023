#!/bin/bash

echo $(dirname $(realpath $0))
cd $(dirname $(realpath $0))


cd ../../../third_party/voronoi_global_planner
python3 vor_node.py