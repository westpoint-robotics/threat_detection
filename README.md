# Requirements
This assumes you are running ubuntu 16.04 and already have darknet/yolo installed.  The regular version of darknet/yolo can either be downloaded by following the instrucitons [here](https://pjreddie.com/darknet/yolo/), or from the westpoint-robotics repo [here](https://github.com/westpoint-robotics/darknet-yolov3).  For the ROS integrated yolo, our local repo is [here](https://github.com/westpoint-robotics/darknet-yolov3-ros).

# Installation of threat detection module
	
	mkdir -p ~/threat_detection/azure/rifle && cd ~/threat_detection
	
	git init && git remote add gh git@github.com:westpoint-robotics/threat_detection.git && git pull gh master

# Datasets
## Download our dataset
[Download here](https://github.com/westpoint-robotics/threat_detection/tree/master/scripts)

## Creating a new dataset
To download new images for making a new dataset follow instructions [here](https://github.com/westpoint-robotics/threat_detection/tree/master/download_images)

To label new class, follow instructions [here](https://github.com/westpoint-robotics/threat_detection/tree/master/YOLOtools)

# Usage
TBD.  We're still working on this part.

