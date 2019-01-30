# YOLO-Annotation-Tool 
(forked from [here](https://github.com/westpoint-robotics/threat_detection/tree/master/scripts) )
## This is for creating the training set of images for YOLO
#### Create 001 folder in Images folder and put your class one images
mkdir -p ~/threat_detection/YOLOtools/Images/002
cp all/your/unlabeled/image ~/threat_detection/YOLOtools/Images/002

#### (Optional) Use these scripts to tweak your images before putting them in the ../Images/0XX folder
Use the rename.py [script](https://github.com/westpoint-robotics/threat_detection/tree/master/scripts) to serialize images and convert them all to jpg. 

Use resize.py to scale images down to better fit on the screen during labeling.  

#### Run Main python script 
	python main.py

When the window opens, type the folder name that contains the unlabeled images (it should be something like "001", "002", etc.)

![Open Project](https://github.com/westpoint-robotics/threat_detection/blob/master/readme_figs/labelingtool_000001.jpg)
# ![Open Project](https://github.com/westpoint-robotics/threat_detection/blob/master/git_ref/get_api_key.jpg)


#### Run convert python file for create final text file for yolo images 
	python convert.py




# Errors
If you get this error when running main.py:

	Traceback (most recent call last):
	  File "main.py", line 12, in <module>
	    from PIL import Image, ImageTk
	ImportError: cannot import name ImageTk

run this: 

	sudo apt-get install -y python-imaging python-imaging-tk


## Bash cruft

	ls *.{png,gif}

	for file in *.JPG
	do
		echo "$file"
		mv "$file" "${file/.JPG/.jpg}"
	done


	for file in *.{png,gif}
	do
		echo "$file"
		# mv "$file" "${file/.JPG/.jpg}"
	done
