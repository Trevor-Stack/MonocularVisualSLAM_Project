# MonocularVisualSLAM_Project
Final project for 16-833

## Downloading the Datasets
The Euroc rosbags can be downloaded [HERE](https://www.research-collection.ethz.ch/entities/researchdata/bcaf173e-5dac-484b-bc37-faf97a594f1f)

The SubT rosbags can be downloaded [HERE](https://superodometry.com/iccv23_challenge_VI)


## Instructions for ORBSLAM3

Install ORBSLAM3 by following the instructions [HERE](https://github.com/UZ-SLAMLab/ORB_SLAM3).

## Instructions for SVO

Install SVO by following the instructions [HERE](https://github.com/uzh-rpg/rpg_svo_pro_open). Build with global map using iSAM2.

Place `/SVO/subt.launch` into the `/src/rpg_svo_pro_open/svo_ros/launch/` directory.

Place `/SVO/subt.yaml` into the `/src/rpg_svo_pro_open/svo_ros/param/calib/` directory.

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
### Converting .bag to .tum files
Place the `svo_eval.bag` file into the `/SVO/` directory and run:
```
python SVO/bag_to_tum_svo.py
```

## Instructions for VinsMono
Install VinsMono by following the instructions [HERE](https://github.com/HKUST-Aerial-Robotics/VINS-Mono)

Place `/VinsMono/subt.launch` into the `/src/VINS-Mono/vins_estimator/launch/` directory.

Place `/VinsMono/subt_config.yaml` into the `/src/VINS-Mono/config/subt/` directory.


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

### Converting .bag to .tum files
Place the `vins_eval.bag` file into the `/VinsMono/` directory and run:
```
python VinsMono/bag_to_tum_vins.py
```

## Getting APE/RPE using EVO

Install EVO:
```
pip install evo
```

Calculating and visulaizing APE and RPE (Example)
```
evo_ape tum VinsMono/vins_tums/laurel_hh2_gt.tum VinsMono/vins_tums/laurel_caverns_hh2_vins_slam.tum -a --plot --plot_mode xyz

evo_rpe tum VinsMono/vins_tums/laurel_hh2_gt.tum VinsMono/vins_tums/laurel_caverns_hh2_vins_slam.tum -a --plot --plot_mode xyz
```

.tum files are provided in `/VinsMono/vins_tums/` and `/SVO/svo_tums/`

## Adding motion blur
Run the file:
```python add_motion_blur.py input outpu --kernel-size i```
where i can be any kernel size 5, 7, 9, 15 (default 15)
