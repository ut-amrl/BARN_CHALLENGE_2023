# Run Instructions for BARN Challenge Organizers !!


## Step 1: Add the following to your `~/.bashrc` to point `ROS_PACKAGE_PATH` to the BARN repo
```
export ROS_PACKAGE_PATH=/path/to/BARN_CHALLENGE_2023:$ROS_PACKAGE_PATH
source ~/.bashrc
```

## Step 2: Run the pre-built singularity container

```
singularity run nav_competition_image.sif
```

## Step 3: Build
```
bash build_packages.sh 
```

## Step 3: Run the run.py file
```
python3 run.py --world_idx 0 
```

# Setup and Install

## Step 1: Clone the repo

```
git clone git@github.com:ut-amrl/BARN_CHALLENGE_2023.git
```

## Step 2: Add the following to your `~/.bashrc` to point `ROS_PACKAGE_PATH` to the BARN repo
```
export ROS_PACKAGE_PATH=/path/to/BARN_CHALLENGE_2023:$ROS_PACKAGE_PATH
source ~/.bashrc
```

## Step 3: Build
```
cd /path/to/BARN_CHALLENGE_2023
bash build_packages.sh 
```

## Step 4: Run
Download the worlds from [**this link**](https://github.com/Daffan/nav-competition-icra2022/tree/main/jackal_helper/worlds/BARN) and place them in `/path/to/BARN_CHALLENGE_2023/jackal_helper/worlds/BARN/`. Then run the following command (first argument indicates the world id and the second argument is the trial run number):

```
python3 run_original.py 1 1
```

# Running with Docker (Do the following after Step 2 above)

## Step 2.5: Setup


### Prerequisites

1. [**Install Docker Engine**](https://docs.docker.com/engine/install/ubuntu)

2. [**Install the Docker Compose V2 Plugin**](https://docs.docker.com/compose/install/linux/)

3. [**Install the NVIDIA Container Toolkit**](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

4. [**Add users to the `docker` group**](https://docs.docker.com/engine/install/linux-postinstall)

### Build

```
git clone git@github.com:ut-amrl/ros-noetic-docker.git
cd /path/to/ros-noetic-docker
./build.py barn
./launch.py barn
```

### Add the following to `~/.bashrc`:

```
[[ -e /dockerrc ]] && source /dockerrc
source ~/.bashrc
```

### Start shell in container
```
docker exec -it $USER-noetic-barn-app-1 bash
```

Continue to Steps 3 and 4 as above
