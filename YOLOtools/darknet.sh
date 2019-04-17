# IMG="/home/benjamin/datasets/test/dog.jpg"
IMG="/home/benjamin/datasets/Aggressiveness/Low_ordered/images/low_aggressive_000003.jpg"


# DATA="/home/benjamin/ros/src/usma_threat_ros/yolo/coco-v3.data"
# CFG="/home/benjamin/ros/src/usma_threat_ros/yolo/coco-v3.cfg"
# WTS="/home/benjamin/ros/src/usma_threat_ros/yolo/coco-v3.weights"

DATA="/home/benjamin/ros/src/usma_threat_ros/yolo/pistol.data"
CFG="/home/benjamin/ros/src/usma_threat_ros/yolo/pistol-tiny.cfg"
WTS="/home/benjamin/ros/src/usma_threat_ros/yolo/pistol-tiny_last.weights"

# DATA="/home/benjamin/darknet/pistol.data"
# WTS="/home/benjamin/darknet/pistol-yolov3-tiny_300000.weights"
# CFG="/home/benjamin/darknet/pistol-yolov3-tiny.cfg"


./darknet detector test $DATA $CFG $WTS $IMG