# package contents
## sub-image_dataset.py
This script is to process a dataset into high-medium-low-zero classifications based on the skeleton and gun positions.

## five_class_dataset.py
This script will process the same dataset into five classes: high-medium-mild-low-zero.  Each image is processed for detecting guns and people, then after they're associated, asks the user to tap a key to identify which category the resulting skeleton belongs.  Folder locations and skeleton models are defined in five_class_dataset.yaml
