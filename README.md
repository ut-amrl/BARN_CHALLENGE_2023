We assume that you have downloaded libtorch and unzipped it in /opt/libtorch/

# Run Steps 0-4 (for BARN Challenge Organizers)

## Step 0: Clone the repo

```
git clone git@github.com:ut-amrl/BARN_CHALLENGE_2023.git
```

## Step 1: Add the following to your `~/.bashrc` to point `ROS_PACKAGE_PATH` to the BARN repo
```
export ROS_PACKAGE_PATH=/path/to/BARN_CHALLENGE_2023:$ROS_PACKAGE_PATH
source ~/.bashrc
```

## Step 2: Build and Run the pre-built singularity container

```
sudo singularity build nav_competition_image.sif Singularity.def
singularity run nav_competition_image.sif
```

## Step 3: Build some required packages inside the container
```
bash build_packages.sh 
```

## Step 4: Add the following to your `~/.bashrc` to setup the workspace
```
source /path/to/BARN_CHALLENGE_2023/devel/setup.bash
```

## Step 5: Run the run.py file
```
python3 run.py --world_idx 0 
```
---

# Setup and Install (for BARN Challenge Participants)

## Without Docker

### Step 1: Clone the repo

```
git clone git@github.com:ut-amrl/BARN_CHALLENGE_2023.git
```

### Step 2: Add the following to your `~/.bashrc` to point `ROS_PACKAGE_PATH` to the BARN repo
```
export ROS_PACKAGE_PATH=/path/to/BARN_CHALLENGE_2023:$ROS_PACKAGE_PATH
```

### Step 3: Build
```
cd /path/to/BARN_CHALLENGE_2023
bash build_packages.sh 
```

## Step 4: Add the following to your `~/.bashrc` to setup the workspace
```
source /path/to/BARN_CHALLENGE_2023/devel/setup.bash
```

## Step 5: Run
Download the worlds from [**this link**](https://github.com/Daffan/nav-competition-icra2022/tree/main/jackal_helper/worlds/BARN) and place them in `/path/to/BARN_CHALLENGE_2023/jackal_helper/worlds/BARN/`. Then run the following command (first argument indicates the world id, second argument is the trial run number, and the third argument is 1 if you want GUI else 0):

```
python3 run_original.py 1 1 1
```
Available flags:
- `--algo`: either "mb" (move_base + graph nav) or "vor" (voronoi + graph nav) {default: "vor"}
- `--param`: either "2022" or "2023" (i.e., this is the parameter to choose in the localgoal.py script) {default: "2023"}
- `--result_dir`: path to the directory where results will be dumped {default: "result"}
- `--world_idx`: world id {default: 0}
- `--gui`: 0 is false and 1 is true {default: 1}
- `--run_idx`: trial run number {default: 0}

To run multiple runs on multiple worlds:
```
bash run_multiple_runs.sh 0 40 0 299 "vor" "2023"
```
where the first two args are for start and end of run_idx, and the next two for start and end of world_idx. So this will do 40 runs over all the worlds for voronoi based planner and with 2023 choice of parameters.

To analyse results generated from `run_multiple_runs.sh`:
```
python analyse_results.py "result_vor_2023" 20
```
where the first argument is the result_dir that contains all the logs, and the second argument represents that it will plot just the top 20 most failed worlds.

## With Docker (Do the following after Step 2 above)

### Step 2.5: Setup

#### Prerequisites

1. [**Install Docker Engine**](https://docs.docker.com/engine/install/ubuntu)

2. [**Install the Docker Compose V2 Plugin**](https://docs.docker.com/compose/install/linux/)

3. [**Install the NVIDIA Container Toolkit**](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

4. [**Add users to the `docker` group**](https://docs.docker.com/engine/install/linux-postinstall)

#### Build

```
git clone git@github.com:ut-amrl/ros-noetic-docker.git
cd /path/to/ros-noetic-docker
./build.py barn
./launch.py barn
```

#### Add the following to `~/.bashrc`:

```
[[ -e /dockerrc ]] && source /dockerrc
source ~/.bashrc
```

#### Start shell in container
```
docker exec -it $USER-noetic-barn-app-1 bash
```

Continue to Steps 3 and 4 as above
