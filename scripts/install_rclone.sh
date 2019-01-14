sudo apt install -y gthumb
cd ~/Downloads && curl -O https://downloads.rclone.org/rclone-current-linux-amd64.zip
unzip rclone-current-linux-amd64.zip && cd rclone-*-linux-amd64

# Copy binary file

sudo cp rclone /usr/bin/ && sudo chown root:root /usr/bin/rclone && sudo chmod 755 /usr/bin/rclone

# Install manpage

sudo mkdir -p /usr/local/share/man/man1 && sudo cp rclone.1 /usr/local/share/man/man1/ && sudo mandb 

# Run rclone config to setup. See rclone config docs for more details.


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
