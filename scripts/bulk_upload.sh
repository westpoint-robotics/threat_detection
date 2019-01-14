tar -cvf ~/datasets/assault_rifle.tar ~/datasets/assault_rifle/* 
tar -cvf ~/datasets/automatic_rifle.tar ~/datasets/automatic_rifle/* 
tar -cvf ~/datasets/hand_gun.tar ~/datasets/hand_gun/* 
tar -cvf ~/datasets/machine_gun.tar ~/datasets/machine_gun/* 
tar -cvf ~/datasets/pistol.tar ~/datasets/pistol/* 
tar -cvf ~/datasets/pistol_in_hand.tar ~/datasets/pistol_in_hand/* 
tar -cvf ~/datasets/rifle.tar ~/datasets/rifle/* 
tar -cvf ~/datasets/shooting.tar ~/datasets/shooting/* 


rclone sync ~/datasets/assault_rifle.tar threatdrive:/Threat_Detection/datasets/ -v
rclone sync ~/datasets/automatic_rifle.tar threatdrive:/Threat_Detection/datasets/ -v
rclone sync ~/datasets/hand_gun.tar threatdrive:/Threat_Detection/datasets/ -v
rclone sync ~/datasets/machine_gun.tar threatdrive:/Threat_Detection/datasets/ -v
rclone sync ~/datasets/pistol.tar threatdrive:/Threat_Detection/datasets/ -v
rclone sync ~/datasets/pistol_in_hand.tar threatdrive:/Threat_Detection/datasets/ -v
rclone sync ~/datasets/rifle.tar threatdrive:/Threat_Detection/datasets/ -v