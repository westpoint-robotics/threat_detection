cd ~/datasets/FullPistolSkeletons/body_mpii/
tar -cvf mpii_skeletons.tar skeleton_threat/* 
mv ~/datasets/FullPistolSkeletons/body_mpii/mpii_skeletons.tar ~/datasets/mpii_skeletons.tar

cd ~/datasets/
tar -cvf FullPistolSkeletons.tar FullPistolSkeletons/* 
rclone sync ~/datasets/FullPistolSkeletons.tar threatdrive:/Threat_Detection/datasets/ -v

cd ~/threat_detection/scripts/

