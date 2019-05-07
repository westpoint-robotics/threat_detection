# import libraries
import sys; sys.path.append('/usr/local/python'); sys.path.append('/usr/local/python')
from openpose import pyopenpose as op

import numpy as np
import cv2
from os import walk # for listing contents of a directory
import yaml

def img_crop(image, x_min, x_max, y_min, y_max):
	cropped_image = image[y_min:y_max, x_min:x_max]
	return cropped_image

def box_overlap(human_box, gun_box):
	# Overlapping rectangles overlap both horizontally & vertically
	x_bool = range_overlap(human_box["xmin"], human_box["xmax"], gun_box["xmin"], gun_box["xmax"])
	y_bool = range_overlap(human_box["ymin"], human_box["ymax"], gun_box["ymin"], gun_box["ymax"])
	return x_bool and y_bool

def range_overlap(a_min, a_max, b_min, b_max):
	# Neither range is completely greater than the other
	return (a_min <= b_max) and (b_min <= a_max)

def main():
	# Setup config
	with open("sub-image_config.yaml", 'r') as ymlfile:
		if sys.version_info[0] > 2:
			cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
		else:
			cfg = yaml.load(ymlfile)

	# Setup openpose
	op_params = dict()
	op_params["model_folder"] = cfg['model_folder']
	op_params["model_pose"] = cfg['model_pose']

	# Starting OpenPose
	opWrapper = op.WrapperPython()
	opWrapper.configure(op_params)
	opWrapper.start()
	datum = op.Datum()

	image_files = []
	for (dirpath, dirnames, filenames) in walk(cfg['image_folder']):
		image_files.extend(filenames)
		break

	# load image and labels
	
	current_image = cfg['image_folder'] + image_files[0]

	cv_image = cv2.imread(current_image,cv2.IMREAD_COLOR) #load image in cv2
	cv_img_height = cv_image.shape[0]
	cv_img_width = cv_image.shape[1]

	
	# print("First image in list: {} : (height, width) = ({},{})").format(image_files[0], cv_img_height, cv_img_width)

	person_lines = []
	pistol_lines = []
	person_boxes = []
	pistol_boxes = []
	with open(cfg['label_folder']+image_files[0][:-4]+".txt") as file:
		for line in file: 
			line = line.strip().split() #or some other preprocessing
			box_center_x = float(line[1])*cv_img_width
			box_center_y = float(line[2])*cv_img_height
			box_width = float(line[3])*cv_img_width
			box_height = float(line[4])*cv_img_height
			x_min = int(round(box_center_x - (box_width/2)))
			x_max = int(round(box_center_x + (box_width/2)))
			y_min = int(round(box_center_y - (box_height/2)))
			y_max = int(round(box_center_y + (box_height/2)))
			if line[0] == "0": # then it is a pistol
				# pistol_boxes.append({'xmin':x_min,'ymin':y_min,'xmax':x_max,'ymax':y_max})
				pistol_boxes.append({'xmin':x_min,'ymin':y_min,'xmax':x_max,'ymax':y_max, 'center_xy':[box_center_x, box_center_y]})
			if line[0] == "1": # then it is a person
				person_boxes.append({'xmin':x_min,'ymin':y_min,'xmax':x_max,'ymax':y_max})
	
	# print("person_boxes: {}").format(person_boxes)
	# print("pistol_boxes: {}").format(pistol_boxes)


	# check overlapping boxes & associate pistols with people
	potential_threats = []
	for person_box in person_boxes:
		for pistol_box in pistol_boxes:
			# if pistol is associated, 
			if box_overlap(person_box, pistol_box):
				potential_threats.append({'xmin':person_box['xmin'],'ymin':person_box['ymin'],'xmax':person_box['xmax'],'ymax':person_box['ymax'], 'pistol_xy':pistol_box['center_xy']})
				# print("potential_threats: {}").format(potential_threats)
				# create raw sub image, 
				cropped = img_crop(cv_image, person_box['xmin'], person_box['xmax'], person_box['ymin'], person_box['ymax'])
				cv2.imshow("cropped", cropped)
				cv2.waitKey(0)
				cv2.destroyWindow("cropped")
				# calculate skeleton
				skel_image = cropped.copy()

	
				datum.cvInputData = skel_image
				opWrapper.emplaceAndPop([datum])

				# save skeleton image
				# add pistol to skeleton 
				# Save numpy arrays
				if cfg['save_skeltons']:
					print("Body keypoints: \n {}").format(datum.poseKeypoints)
					keypoint_file = cfg['keypoint_folder']+"keypoints_{}".format(keypoints_generated)
					np.save(keypoint_file, datum.poseKeypoints)
					keypoints_generated += 1




if __name__ == "__main__":
	main()

	# 	# print("box center (x,y), box (h,w) : ({}, {}) ({}, {})").format(box_center_x, box_center_y, box_width, box_height)
	# 	# x,y are rectangle center and width and height
	# 	# cv2.circle(cv_image, (int(box_center_x),int(box_center_y)), 5, (255,0,0), thickness=2, lineType=8, shift=0) 
	# 	cv2.imshow("img_crop", img_crop(cv_image, x_min, x_max, y_min, y_max))
	# 	cv2.waitKey(0)
	# 	cv2.destroyWindow("img_crop")


	# cv2.imshow("cv_image", cv_image)
	# cv2.waitKey(0)
	# cv2.destroyWindow("cv_image")