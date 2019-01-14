cd ~/datasets

tar -cvf assault_rifle.tar assault_rifle/* 
tar -cvf automatic_rifle.tar automatic_rifle/* 
tar -cvf hand_gun.tar hand_gun/* 
tar -cvf machine_gun.tar machine_gun/* 
tar -cvf pistol.tar pistol/* 
tar -cvf pistol_in_hand.tar pistol_in_hand/* 
tar -cvf rifle.tar rifle/* 
tar -cvf shooting.tar shooting/* 


rclone sync ~/datasets/assault_rifle.tar threatdrive:/Threat_Detection/datasets/ -v
rclone sync ~/datasets/automatic_rifle.tar threatdrive:/Threat_Detection/datasets/ -v
rclone sync ~/datasets/hand_gun.tar threatdrive:/Threat_Detection/datasets/ -v
rclone sync ~/datasets/machine_gun.tar threatdrive:/Threat_Detection/datasets/ -v
rclone sync ~/datasets/pistol.tar threatdrive:/Threat_Detection/datasets/ -v
rclone sync ~/datasets/pistol_in_hand.tar threatdrive:/Threat_Detection/datasets/ -v
rclone sync ~/datasets/rifle.tar threatdrive:/Threat_Detection/datasets/ -v
rclone sync ~/datasets/shooting.tar threatdrive:/Threat_Detection/datasets/ -v

