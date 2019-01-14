# YOLO-Annotation-Tool
## This is for creating the training set of images for YOLO

###### Commands on terminal:
```
git clone https://github.com/ManivannanMurugavel/YOLO-Annotation-Tool.git

cd YOLO-Annotation-Tool
```
### Create 001 folder in Images folder and put your class one images

### Convert to .JPEG from any type of images. Use this command(Ubuntu)

	sudo apt-get -y install imagemagick

	mogrify -format jpg *.jpg*
	
	mogrify -format jpg *.jpeg

	mogrify -format jpg *.JPG




```mogrify -format jpg *.JPEG```
or
```mogrify -format jpg *.jpeg```
or
```mogrify -format jpg *.png```

### Run Main python script 

 ``` python main.py ```

### Run convert python file for create final text file for yolo images 

```python convert.py```
# -------Progress-------


# Bash cruft

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


# Errors
If you get this error when running main.py:

	Traceback (most recent call last):
	  File "main.py", line 12, in <module>
	    from PIL import Image, ImageTk
	ImportError: cannot import name ImageTk

run this: 

	sudo apt-get install -y python-imaging python-imaging-tk