# import libraries
import sys; sys.path.append('/usr/local/python')
import numpy as np
import cv2
import os
import yaml
from openpose import pyopenpose as op


#setup and import darknet-yolo
sys.path.append('/usr/local/python') # path for CMUopenpose library
sys.path.append(os.environ['DARKNET_PATH']) 
sys.path.append(os.environ['DARKNET_PATH']+'/python')
import darknet as dn

def get_bounding_boxes(detections, box_color):
	boxes = []
	for detection in detections:
		bounds = detection[2]
		box = {
			"box_color" : box_color,
			"class" : detection[0],
			"probability" : detection[1],
			"xmin" : int(bounds[0] - bounds[2]/2),
			"ymin" : int(bounds[1] - bounds[3]/2),
			"xmax" : int(bounds[0] + bounds[2]/2),
			"ymax" : int(bounds[1] + bounds[3]/2)
			}
		boxes.append(box)
	return boxes

def box_overlap(human_box, gun_box):
	# Overlapping rectangles overlap both horizontally & vertically
	x_bool = range_overlap(human_box["xmin"], human_box["xmax"], gun_box["xmin"], gun_box["xmax"])
	y_bool = range_overlap(human_box["ymin"], human_box["ymax"], gun_box["ymin"], gun_box["ymax"])
	return x_bool and y_bool

def range_overlap(a_min, a_max, b_min, b_max):
	# Neither range is completely greater than the other
	return (a_min <= b_max) and (b_min <= a_max)

def imcrop(img, bbox):
   x1, y1, x2, y2 = bbox
   if x1 < 0 or y1 < 0 or x2 > img.shape[1] or y2 > img.shape[0]:
        img, x1, x2, y1, y2 = pad_img_to_fit_bbox(img, x1, x2, y1, y2)
   return img[y1:y2, x1:x2, :]

def main():
	# Setup yolo config
	with open("yolo_config.yml", 'r') as ymlfile:
		if sys.version_info[0] > 2:
			cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
		else:
			cfg = yaml.load(ymlfile)

	yolo_data = cfg['yolo_data'] 
	yolo_config = cfg['yolo_config'] 
	yolo_weights = cfg['yolo_weights'] 
	pistol_net = dn.load_net(yolo_config,yolo_weights,0)
	pistol_meta = dn.load_meta(yolo_data)

	coco_data = cfg['coco_data'] 
	coco_config = cfg['coco_config'] 
	coco_weights = cfg['coco_weights'] 
	coco_net = dn.load_net(coco_config,coco_weights,0)
	coco_meta = dn.load_meta(coco_data)

	# setup openpose config
	with open("openpose_config.yml", 'r') as opymlfile:
		if sys.version_info[0] > 2:
			op_cfg = yaml.load(opymlfile, Loader=yaml.FullLoader)
		else:
			op_cfg = yaml.load(opymlfile)
	# Custom Params (refer to include/openpose/flags.hpp for more parameters)
	op_params = dict()
	op_params["model_folder"] = op_cfg['model_folder']
	op_params["model_pose"] = op_cfg['model_pose']

	# Starting OpenPose
	opWrapper = op.WrapperPython()
	opWrapper.configure(op_params)
	opWrapper.start()
	datum = op.Datum()

	# Load image
	cv_image = cv2.imread(cfg['single_image'] ,cv2.IMREAD_COLOR) #load image in cv2
	box_image = cv_image.copy()
	skeleton_image = cv2.resize(box_image,(dn.network_width(pistol_net),dn.network_height(pistol_net)),interpolation=cv2.INTER_LINEAR)

	# Detect objects
	frame_resized = cv2.resize(box_image,(dn.network_width(pistol_net),dn.network_height(pistol_net)),interpolation=cv2.INTER_LINEAR)
	darknet_image = dn.make_image(dn.network_width(pistol_net),dn.network_height(pistol_net),3)
	dn.copy_image_from_bytes(darknet_image,frame_resized.tobytes())
	pistol_detections = dn.detect_image(pistol_net, pistol_meta, darknet_image, thresh=0.25)
	coco_detections = dn.detect_image(coco_net, coco_meta, darknet_image, thresh=0.25)
	
	# get bounding boxes
	pistol_boxes = get_bounding_boxes(pistol_detections, (255,0,0))
	coco_boxes = get_bounding_boxes(coco_detections, (0,0,255))
	BBoxes = []
	for box in pistol_boxes:
		BBoxes.append(box)
	for box in coco_boxes:
		BBoxes.append(box)

	box_color = (255,0,0)
	for box in pistol_boxes:
		# print("pistol_boxes  {}").format(box['class'])
		upper_left = (box['xmin'],box['ymin'])
		lower_right = (box['xmax'],box['ymax'])
		cv2.rectangle(frame_resized,upper_left,lower_right,box_color,2)

	box_color = (0,0,255)
	for box in coco_boxes:
		# print("coco_boxes  {}").format(box['class'])
		upper_left = (box['xmin'],box['ymin'])
		lower_right = (box['xmax'],box['ymax'])
		cv2.rectangle(frame_resized,upper_left,lower_right,box_color,2)

	box_image = cv2.resize(frame_resized,(cv_image.shape[1], cv_image.shape[0]),interpolation=cv2.INTER_LINEAR)	

	# cv2.imshow("box_image", box_image)
	# cv2.waitKey(0)
	# cv2.destroyWindow("box_image")

	# check overlapping boxes
	person_boxes = []
	pistol_boxes = []
	potential_threats = []
	for box in BBoxes:
		print("box[class] = {}").format(box)
		if box['class'] == "person":
			person_boxes.append({'xmin':box['xmin'],'ymin':box['ymin'],'xmax':box['xmax'],'ymax':box['ymax']})

		if box['class'] == "pistol":
			pistol_boxes.append({'xmin':box['xmin'],'ymin':box['ymin'],'xmax':box['xmax'],'ymax':box['ymax']})

	for person_box in person_boxes:
		for pistol_box in pistol_boxes:
			if box_overlap(person_box, pistol_box):
				potential_threats.append(person_box)

	
	
	for person_box in potential_threats:
		# generate sub images for skeleton
		crop_img = skeleton_image[person_box["ymin"]:person_box["ymax"],  person_box["xmin"]:person_box["xmax"]]
		# cv2.imshow("crop_img", crop_img)
		# cv2.waitKey(0)
		# cv2.destroyWindow("crop_img")
		
		# process sub image for skeleton		
		skel_image = crop_img.copy()
		datum.cvInputData = skel_image
		opWrapper.emplaceAndPop([datum])

		cv2.imshow("skeleton", datum.cvOutputData)
		cv2.waitKey(0)
		cv2.destroyWindow("skeleton")

		datum.poseKeypoints



	
	
	# imageToProcess = cv2.imread(current_image)
	# datum.cvInputData = imageToProcess
	# opWrapper.emplaceAndPop([datum])



if __name__ == "__main__":
	main()
