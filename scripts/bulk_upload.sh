cd ~/threat_detection/datasets/Aggressiveness

tar -cvf Low_ordered.tar Low_ordered/* 
tar -cvf High_ordered.tar High_ordered/* 
tar -cvf Medium_ordered.tar Medium_ordered/* 

rclone sync ~/threat_detection/datasets/Aggressiveness/Low_ordered.tar threatdrive:/Threat_Detection/datasets/Aggressiveness/ -v
rclone sync ~/threat_detection/datasets/Aggressiveness/High_ordered.tar threatdrive:/Threat_Detection/datasets/Aggressiveness/ -v
rclone sync ~/threat_detection/datasets/Aggressiveness/Medium_ordered.tar threatdrive:/Threat_Detection/datasets/Aggressiveness/ -v


# tar -cvf assault_rifle.tar assault_rifle/* 
# tar -cvf automatic_rifle.tar automatic_rifle/* 
# tar -cvf hand_gun.tar hand_gun/* 
# tar -cvf machine_gun.tar machine_gun/* 
# tar -cvf pistol.tar pistol/* 
# tar -cvf pistol_in_hand.tar pistol_in_hand/* 
# tar -cvf rifle.tar rifle/* 
# tar -cvf shooting.tar shooting/* 

# tar -cvf pistol_yolo.tar pistol_yolo/* cd ~/datasets


# tar -cvf pistol_labeled.tar labeled/pistol_yolo/* 


# rclone sync ~/datasets/assault_rifle.tar threatdrive:/Threat_Detection/datasets/ -v
# rclone sync ~/datasets/automatic_rifle.tar threatdrive:/Threat_Detection/datasets/ -v
# rclone sync ~/datasets/hand_gun.tar threatdrive:/Threat_Detection/datasets/ -v
# rclone sync ~/datasets/machine_gun.tar threatdrive:/Threat_Detection/datasets/ -v
# rclone sync ~/datasets/pistol.tar threatdrive:/Threat_Detection/datasets/ -v
# rclone sync ~/datasets/pistol_in_hand.tar threatdrive:/Threat_Detection/datasets/ -v
# rclone sync ~/datasets/rifle.tar threatdrive:/Threat_Detection/datasets/ -v
# rclone sync ~/datasets/shooting.tar threatdrive:/Threat_Detection/datasets/ -v

# rclone sync ~/datasets/pistol_yolo.tar threatdrive:/Threat_Detection/datasets/ -v

# rclone sync ~/datasets/pistol_labeled.tar threatdrive:/Threat_Detection/datasets/ -v
