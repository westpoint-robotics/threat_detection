mkdir -p ~/datasets && cd ~/datasets

rclone sync threatdrive:/Threat_Detection/datasets/assault_rifle.tar ~/datasets -v
rclone sync threatdrive:/Threat_Detection/datasets/automatic_rifle.tar ~/datasets -v
rclone sync threatdrive:/Threat_Detection/datasets/hand_gun.tar ~/datasets -v
rclone sync threatdrive:/Threat_Detection/datasets/machine_gun.tar ~/datasets -v
rclone sync threatdrive:/Threat_Detection/datasets/pistol.tar ~/datasets -v
rclone sync threatdrive:/Threat_Detection/datasets/pistol_in_hand.tar ~/datasets -v
rclone sync threatdrive:/Threat_Detection/datasets/rifle.tar ~/datasets -v
rclone sync threatdrive:/Threat_Detection/datasets/shooting.tar ~/datasets -v

tar xf assault_rifle.tar
tar xf automatic_rifle.tar
tar xf hand_gun.tar
tar xf machine_gun.tar
tar xf pistol.tar
tar xf pistol_in_hand.tar
tar xf rifle.tar
tar xf shooting.tar
