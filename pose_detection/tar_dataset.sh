tar -czvf FullPistolSkeletons.tar.gz FullPistolSkeletons

rclone sync ~/datasets/FullPistolSkeletons.tar.gz threatdrive:/Threat_Detection/datasets/Aggressiveness/ -v



tar -czvf Aggressiveness_old.tar.gz Aggressiveness

rclone sync ~/datasets/Aggressiveness_old.tar.gz threatdrive:/Threat_Detection/datasets/Aggressiveness/ -v
