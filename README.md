# MonocularVisualSLAM_Project
Final project for 16-833


## Instructions for SVO

Install SVO by following the instructions [HERE](https://github.com/uzh-rpg/rpg_svo_pro_open). Build with global map using iSAM2

### In Terminal 1:
```
source /opt/ros/melodic/setup.bash
source /svo_ws/devel/setup.bash 
roscore
```
### In Terminal 2:
```
source /opt/ros/melodic/setup.bash
source /svo_ws/devel/setup.bash 
roslaunch svo_ros euroc_global_map_mono.launch

# Or for Subt
roslaunch svo_ros subt.launch
```

### In Terminal 3 (To record results into a .bag file):
```
source /opt/ros/melodic/setup.bash
source /svo_ws/devel/setup.bash 
rosbag record -O svo_eval.bag /svo/pose_imu /svo/backend_pose_imu /vicon/firefly_sbx/firefly_sbx
```

### In Terminal 4:
```
source /opt/ros/melodic/setup.bash
source /svo_ws/devel/setup.bash 
cd <DATA_DIRECTORY>
rosbag play <ROSBAG_NAME>

# Or to play rosbags sequentially
for bag in $(ls -v *.bag); do
  rosbag play "$bag"
done
```


## Instructions for VinsMono
Install VinsMono by following the instructions [HERE](https://github.com/HKUST-Aerial-Robotics/VINS-Mono)


### In Terminal 1:
```
source /opt/ros/melodic/setup.bash
source /vins_ws/devel/setup.bash 
roscore
```

### In Terminal 2:
```
source /opt/ros/melodic/setup.bash
source /vins_ws/devel/setup.bash 
roslaunch vins_estimator euroc.launch

# Or for SubT
roslaunch vins_estimator subt.launch
```

### In Terminal 3:
```
source /opt/ros/melodic/setup.bash
source /vins_ws/devel/setup.bash 
roslaunch vins_estimator vins_rviz.launch
```

### In Terminal 4 (To record results into a .bag file): 
```
source /opt/ros/melodic/setup.bash
source /vins_ws/devel/setup.bash 
rosbag record -O vins_eval.bag /vins_estimator/odometry /pose_graph/pose_graph_path /vicon/firefly_sbx/firefly_sbx
```

### In Terminal 5 
```
source /opt/ros/melodic/setup.bash
source /vins_ws/devel/setup.bash 
cd <DATA_DIRECTORY>
rosbag play <ROSBAG_NAME>

# Or to play rosbags sequentially
for bag in $(ls -v *.bag); do
  rosbag play "$bag"
done
```