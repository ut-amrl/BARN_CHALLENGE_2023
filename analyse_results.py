import os
import matplotlib.pyplot as plt
import sys

logs_dir = sys.argv[1]
num_worlds_to_plot = int(sys.argv[2])

# logs_dir = "result_vor_2023"
log_files = os.listdir(logs_dir)
log_paths = [logs_dir + "/" + f for f in log_files]

num_results_runs = {}
for i in range(len(log_files)):
    num_results_runs[i] = [0, 0, 0]  # s, t, c
num_results_worlds = {}
for i in range(300):
    num_results_worlds[i] = [0, 0, 0]  # s, t, c

for p in log_paths:
    r = int(p.split("run_")[-1].split(".")[0])
    with open(p, "r") as f:
        w = 0
        while True:
            line = f.readline()
            if not line:
                break
            if "succeeded" in line:
                num_results_runs[r][0] += 1
                num_results_worlds[w][0] += 1
            elif "timeout" in line:
                num_results_runs[r][1] += 1
                num_results_worlds[w][1] += 1
            else:
                num_results_runs[r][2] += 1
                num_results_worlds[w][2] += 1
            w += 1

runs_collides = []
runs_succeeds = []
runs_timeouts = []
for i in range(len(log_files)):
    runs_succeeds.append(num_results_runs[i][0])
    runs_timeouts.append(num_results_runs[i][1])
    runs_collides.append(num_results_runs[i][2])


plt.figure(0)
plt.plot(runs_succeeds, label="succeeded", color="g")
plt.plot(runs_timeouts, label="timeout", color="b")
plt.plot(runs_collides, label="collides", color="r")
plt.legend(loc="upper left")
plt.title("By Runs")
plt.xlabel("Run Number")
plt.ylabel("Results")
plt.savefig("results_by_runs.png")

worlds_idx = []
worlds_fails = []
NUM_WORLDS_NOT_PERFECT = 0
for i in range(300):
    worlds_idx.append(i)
    worlds_fails.append(num_results_worlds[i][1] + num_results_worlds[i][2])
    if worlds_fails[i] > 0:
        NUM_WORLDS_NOT_PERFECT += 1

print(f"Number of worlds it failed atleast once = {NUM_WORLDS_NOT_PERFECT}")
runs_succeeds.sort()


def sort_by_second_list(list1, list2):
    zipped_pairs = zip(list2, list1)
    l1 = []
    l2 = []
    for y, x in sorted(zipped_pairs):
        l1.append(x)
        l2.append(y)
    return l1, l2


worlds_idx, worlds_fails = sort_by_second_list(worlds_idx, worlds_fails)
worlds_idx.reverse()
worlds_fails.reverse()

worlds_succeeds = []
worlds_collides = []
worlds_timeouts = []
for i in worlds_idx:
    worlds_succeeds.append(num_results_worlds[i][0])
    worlds_timeouts.append(num_results_worlds[i][1])
    worlds_collides.append(num_results_worlds[i][2])

worlds_idx = [str(i) for i in worlds_idx]

toPlot = num_worlds_to_plot

plt.figure(1)
plt.bar(worlds_idx[:toPlot], worlds_collides[:toPlot], color="r", label="collides")
plt.bar(worlds_idx[:toPlot], worlds_timeouts[:toPlot], color="b", bottom=worlds_collides[:toPlot], label="timeouts")
plt.bar(worlds_idx[:toPlot], worlds_succeeds[:toPlot], color="g", bottom=worlds_fails[:toPlot], label="succeeded")
plt.legend(loc="upper right")
plt.title("By Worlds - Top " + str(toPlot) + " Most Failed Worlds")
plt.xlabel("World Number")
plt.ylabel("Number of Failures")
plt.ylim(top=len(log_files)-1)
plt.xticks(rotation="vertical")
plt.savefig("results_by_worlds.png")

plt.show()
