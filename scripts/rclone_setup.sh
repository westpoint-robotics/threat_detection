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

rclone config


rclone sync ~/datasets/shooting threatdrive:/Threat_Detection/shooting/ -v


sudo apt install gthumb

