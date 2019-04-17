# import libraries
import numpy as np
import cv2
import os,sys
import yaml

#setup and import darknet-yolo
sys.path.append('/usr/local/python') # path for CMUopenpose library
sys.path.append(os.environ['DARKNET_PATH']) 
sys.path.append(os.environ['DARKNET_PATH']+'/python')
import darknet as dn

def get_bounding_boxes(detections):
	boxes = []
	for detection in detections:
		bounds = detection[2]
		box = {
			"class" : detection[0],
			"probability" : detection[1],
			"xmin" : int(bounds[0] - bounds[2]/2),
			"ymin" : int(bounds[1] - bounds[3]/2),
			"xmax" : int(bounds[0] + bounds[2]/2),
			"ymax" : int(bounds[1] + bounds[3]/2)
			}
		boxes.append(box)
	return boxes

def main():
	with open("yolo_config.yml", 'r') as ymlfile:
		if sys.version_info[0] > 2:
			cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
		else:
			cfg = yaml.load(ymlfile)

	# Setup yolo config
	yolo_data = cfg['yolo_data'] 
	yolo_config = cfg['yolo_config'] 
	yolo_weights = cfg['yolo_weights'] 
	net = dn.load_net(yolo_config,yolo_weights,0)
	meta = dn.load_meta(yolo_data)

	coco_data = cfg['coco_data'] 
	coco_config = cfg['coco_config'] 
	coco_weights = cfg['coco_weights'] 
	coco_net = dn.load_net(coco_config,coco_weights,0)
	coco_meta = dn.load_meta(coco_data)

	img = cv2.imread(cfg['single_image'] ,cv2.IMREAD_COLOR) #load image in cv2
	objects = dn.detect(net, meta, cfg['single_image']) # from filename
	coco_objects = dn.detect(coco_net, coco_meta, cfg['single_image']) # from filename
	# objects = dn.detect(net, meta, img) #opencv image
	
	# get bounding boxes
	boundingboxes = get_bounding_boxes(objects)
	coco_boxes = get_bounding_boxes(coco_objects)

	# check overlapping boxes
	box_color = (255,0,0)
	for box in boundingboxes:
		print("boundingboxes  {}").format(box['class'])
		upper_left = (box['xmin'],box['ymin'])
		lower_right = (box['xmax'],box['ymax'])
		cv2.rectangle(img,upper_left,lower_right,box_color,2)

	box_color = (0,0,255)
	for box in coco_boxes:
		print("coco_boxes  {}").format(box['class'])
		upper_left = (box['xmin'],box['ymin'])
		lower_right = (box['xmax'],box['ymax'])
		cv2.rectangle(img,upper_left,lower_right,box_color,2)

		
	cv2.imshow("image", img)
	cv2.waitKey(0)
	cv2.destroyWindow("image")

	# for overlapping pairs, calculate skeletons
	# 


if __name__ == "__main__":
	main()
