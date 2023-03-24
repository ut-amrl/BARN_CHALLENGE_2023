import json 
import os
DIR1 = "/home/alienwareamrl/Research/BARN_CHALLENGE_2023/result/run_3/"


fail1 = []
files = os.listdir(DIR1)
for path in files:
    file = os.path.join(DIR1, path)
    with open(file, 'r') as f:
        data = json.load(f)
        if data[1] != 'succeeded':
            print(data)
            fail1.append(data)