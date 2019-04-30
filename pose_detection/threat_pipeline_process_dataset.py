# import libraries
import sys; sys.path.append('/usr/local/python'); sys.path.append('/usr/local/python')
import numpy as np
import cv2
import os
from os import walk # for listing contents of a directory
import yaml
from openpose import pyopenpose as op

#setup and import darknet-yolo
sys.path.append('/usr/local/python') # path for CMUopenpose library
sys.path.append(os.environ['DARKNET_PATH']) 
sys.path.append(os.environ['DARKNET_PATH']+'/python')
import darknet as dn

import tensorflow as tf
from feedforward_model import *

def prediction(skele,model_name='basic_model'):
	labels = ['high','med','low']
	session = tf.Session()
	with session as sess:
		new_saver = tf.train.import_meta_graph('model/{}.meta'.format(model_name))
		new_saver.restore(sess, 'model/{}'.format(model_name))
		graph = tf.get_default_graph()
		input_ph = graph.get_tensor_by_name("input_ph:0")
		pred = graph.get_tensor_by_name("pred:0")

		predictions = sess.run([pred],feed_dict={input_ph: skele})
		return labels[predictions[0][0]]

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

	# Generate image list
	image_list = []
	for (dirpath, dirnames, filenames) in walk(op_cfg['image_folder']):
		image_list.extend(filenames)
		break

	# Load images
	images_processed = 0
	keypoints_generated = 0
	pistols_detected = 0
	for image in image_list:
		current_image = op_cfg['image_folder']+image
		print("current_image: {}").format(current_image)
		
		cv_image = cv2.imread(current_image,cv2.IMREAD_COLOR) #load image in cv2
		height = cv_image.shape[0]
		width = cv_image.shape[1]
		# print("original height: {}").format(height)
		# print("original width: {}").format(width)
		box_image = cv_image.copy()
		#resize image to match network dimensions
		skeleton_image = cv2.resize(box_image,(dn.network_width(pistol_net),dn.network_height(pistol_net)),interpolation=cv2.INTER_LINEAR)

		# Detect objects
		frame_resized = cv2.resize(box_image,(dn.network_width(pistol_net),dn.network_height(pistol_net)),interpolation=cv2.INTER_LINEAR)
		darknet_image = dn.make_image(dn.network_width(pistol_net),dn.network_height(pistol_net),3)
		dn.copy_image_from_bytes(darknet_image,frame_resized.tobytes())
		pistol_detections = dn.detect_image(pistol_net, pistol_meta, darknet_image, thresh=0.25)
		coco_detections = dn.detect_image(coco_net, coco_meta, darknet_image, thresh=0.25)

		# print("resized height: {}").format(dn.network_height(pistol_net))
		# print("resized width: {}").format(dn.network_width(pistol_net))

		height_scale = float(cv_image.shape[0]) / dn.network_height(pistol_net)
		width_scale = float(cv_image.shape[1]) / dn.network_height(pistol_net)

		# print("height_scale: {}").format(height_scale)
		# print("width_scale: {}").format(width_scale)

		# get bounding boxes
		pistol_boxes = get_bounding_boxes(pistol_detections, (255,0,0))
		coco_boxes = get_bounding_boxes(coco_detections, (0,0,255))
		BBoxes = []
		for box in pistol_boxes:
			BBoxes.append(box)
		for box in coco_boxes:
			BBoxes.append(box)

		fontFace = cv2.FONT_HERSHEY_DUPLEX
		text_color = (0,0,255)
		fontScale = 1
		text_thickness = 1

		box_thickness = 2
		box_color = (255,0,0)
		for box in pistol_boxes:
			if box['class'] == "pistol":
				upper_left = (box['xmin'],box['ymin'])
				lower_right = (box['xmax'],box['ymax'])
				cv2.rectangle(frame_resized,upper_left,lower_right,box_color,box_thickness)
				cv2.putText(frame_resized,box['class'],upper_left, fontFace, fontScale, box_color,text_thickness,cv2.LINE_AA)
				pistols_detected += 1
			
				# cv2.imshow("frame_resized", frame_resized)
				# cv2.waitKey(0)
				# cv2.destroyWindow("frame_resized")


		box_color = (0,0,255)
		for box in coco_boxes:
			# print("coco_boxes  {}").format(box['class'])
			if box['class'] == "person":
				upper_left = (box['xmin'],box['ymin'])
				lower_right = (box['xmax'],box['ymax'])
				cv2.rectangle(frame_resized,upper_left,lower_right,box_color,box_thickness)
				cv2.putText(frame_resized,box['class'],upper_left, fontFace, fontScale, box_color,text_thickness,cv2.LINE_AA)

		# check overlapping boxes
		person_boxes = []
		pistol_boxes = []
		potential_threats = []
		for box in BBoxes:
			# print("box[class] = {}").format(box)
			if box['class'] == "person":
				person_boxes.append({'xmin':box['xmin'],'ymin':box['ymin'],'xmax':box['xmax'],'ymax':box['ymax']})

			if box['class'] == "pistol":
				pistol_boxes.append({'xmin':box['xmin'],'ymin':box['ymin'],'xmax':box['xmax'],'ymax':box['ymax']})

		for person_box in person_boxes:
			for pistol_box in pistol_boxes:
				if box_overlap(person_box, pistol_box):
					potential_threats.append(person_box)

		person_number = 0
		for person_box in potential_threats:
			person_number +=1
			# generate sub images for skeleton
			if (person_box["ymin"] < 0):
				person_box["ymin"] = 0
			if (person_box["xmin"] < 0):
				person_box["xmin"] = 0

			if (person_box["ymax"] > skeleton_image.shape[0]):
				person_box["ymax"] = skeleton_image.shape[0]
			if (person_box["xmax"] > skeleton_image.shape[1]):
				person_box["xmax"] = skeleton_image.shape[0]
			crop_img = skeleton_image[person_box["ymin"]:person_box["ymax"],  person_box["xmin"]:person_box["xmax"]]

			# rescale sub image back to original dimensions
			crop_img_height = crop_img.shape[0]
			crop_img_width = crop_img.shape[1]
			# print("crop_img_width * width_scale : {}*{}={}").format(crop_img_width, width_scale, crop_img_width*width_scale)
			# print("crop_img_height * height_scale : {}*{}={}").format(crop_img_height, height_scale, crop_img_height*height_scale)
			newX,newY = crop_img_width*width_scale, crop_img_height*height_scale
			if (newX > 0) and (newY > 0):
				# process sub image for skeleton		
				skel_image = cv2.resize(crop_img,(int(newX),int(newY)))

				datum.cvInputData = skel_image
				opWrapper.emplaceAndPop([datum])

				# Save numpy arrays
				if op_cfg['save_keypoints']:
					print("Body keypoints: \n {}").format(datum.poseKeypoints)
					keypoint_file = op_cfg['keypoint_folder']+"keypoints_{}".format(keypoints_generated)
					np.save(keypoint_file, datum.poseKeypoints)
					keypoints_generated += 1

		images_processed += 1
		if images_processed%100 == 0:
			print("\n    Images to process remaining in {} : {} \n").format(cfg['image_folder'], len(image_list)-images_processed)

	print("total number of pistols detected, correct or incorrect: {}").format(pistols_detected)	

if __name__ == "__main__":
	main()


