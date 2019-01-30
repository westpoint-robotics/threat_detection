# YOLO-Annotation-Tool 
(forked from [here](https://github.com/westpoint-robotics/threat_detection/tree/master/scripts) )
## This is for creating the training set of images for YOLO
#### Create 001 folder in Images folder and put your class one images
mkdir -p ~/threat_detection/YOLOtools/Images/002
cp all/your/unlabeled/image ~/threat_detection/YOLOtools/Images/002

#### (Optional) Use these scripts to tweak your images before putting them in the ../Images/0XX folder
Use the [rename.py](https://github.com/westpoint-robotics/threat_detection/tree/master/scripts) script to serialize images and convert them all to jpg. 

Use [resize.py](https://github.com/westpoint-robotics/threat_detection/tree/master/scripts) to scale images down to better fit on the screen during labeling.  

#### Run Main python script 
	python main.py

When the window opens, type the folder name that contains the unlabeled images (it should be something like "001", "002", etc.)

![Open Project](https://github.com/westpoint-robotics/threat_detection/blob/master/YOLOtools/readme_figs/labelingtool_000001.jpg)


#### Run convert python file for create final text file for yolo images 
This will generate a series of text files associated with the topleft and bottom right bounding box label, which needs to be converted to the yolo format:

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
