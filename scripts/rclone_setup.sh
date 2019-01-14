rclone config

echo "(n)ew"
echo "threatdrive"
echo "12"
echo "blank"
echo "blank"
echo "1 - full access"
echo "blank"
echo "blank"
echo "(n)o - do not edit advanced config"
echo "(y)es - use auto config"
echo "(n)o - not a team drive"
echo "(y)es this is okay"
echo "(q)uit"





sudo apt install -y gthumb




rclone sync ~/datasets/assault_rifle/ threatdrive:/Threat_Detection/datasets/assault_rifle/ -v
rclone sync ~/datasets/automatic_rifle/ threatdrive:/Threat_Detection/datasets/automatic_rifle/ -v
rclone sync ~/datasets/hand_gun/ threatdrive:/Threat_Detection/datasets/hand_gun/ -v
rclone sync ~/datasets/machine_gun/ threatdrive:/Threat_Detection/datasets/machine_gun/ -v
rclone sync ~/datasets/pistol/ threatdrive:/Threat_Detection/datasets/pistol/ -v
rclone sync ~/datasets/pistol_in_hand/ threatdrive:/Threat_Detection/datasets/pistol_in_hand/ -v
rclone sync ~/datasets/rifle/ threatdrive:/Threat_Detection/datasets/rifle/ -v
rclone sync ~/datasets/shooting/ threatdrive:/Threat_Detection/datasets/shooting/ -v