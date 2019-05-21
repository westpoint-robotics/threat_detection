# Download our dataset
## Download manually 
from [google drive](https://drive.google.com/open?id=1QgnNfyWJurA1RAfc6iIYCJJZpKYNbmu6)

## Download automatically using :
(This will only work if you are me, it requires access to my google drive)

	cd ~/threat_detection/scripts
	. install_rclone.sh

### When prompted at decision points during installation, using these configurations should make other scripts in this repo function properly:
	
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


### using rclone, download datasets and unzip them

	bash ./bulk_download.sh


# To use undupe library
You may need to create a number of folders and directories to use the undupe script.  Call using

	python UH.py

This loads images, scales them down to 10,000 square pixels, then computes ransac homographies to check if images are similar.

	sudo apt install python3-pip
	pip install opencv-python --user
	pip install scikit-image --user


# package contents : a collection of file management scripts
## rename.py
Use this script to rename a folder of images to have a common prefix and a six digit serialization.  Use rename_config.yml to change folders

	<!-- directory of folder with original file name (ends with '/') -->
	original_path: /home/benjamin/threat_detection/datasets/Aggressiveness/Low/
	<!-- original_path: /home/benjamin/threat_detection/YOLOtools/readme_figs/ -->

	<!-- where to put renamed images (ends with '/') -->
	renamed_path: /home/benjamin/threat_detection/datasets/Aggressiveness/Low_ordered/
	<!-- renamed_path: /home/benjamin/threat_detection/YOLOtools/ -->

	<!-- numbers will be appended, suggests ends with '_' -->
	renamed_prefix: low_aggressive_

