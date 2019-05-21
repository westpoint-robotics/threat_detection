# import libraries
import sys; sys.path.append('/usr/local/python'); 
from openpose import pyopenpose as op

import numpy as np
import cv2
from os import walk # for listing contents of a directory
import yaml
import random
from shutil import copyfile # for copying duplicates to folder (for now)
from shutil import move # for moving duplicates to folder (eventually)

def show_keypoints_on_image(image, joints):
	joint_image = image.copy()
	for joint in joints:
		if joint.all():
			# print("joint (x,y): ({}, {})").format(joint[0], joint[1])
			# random joint color
			# cv2.circle(joint_image, (int(joint[0]),int(joint[1])), 4, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), thickness=-1, lineType=8, shift=0) 
			# black joint color with white center
			cv2.circle(joint_image, (int(joint[0]),int(joint[1])), 5, (0,0,0), thickness=-1, lineType=8, shift=0) 
			cv2.circle(joint_image, (int(joint[0]),int(joint[1])), 2, (255,255,255), thickness=-1, lineType=8, shift=0) 

	cv2.circle(joint_image, (int(joints[25][0]),int(joints[25][1])), 8, (0,0,255), thickness=-1, lineType=8, shift=0) 
	cv2.circle(joint_image, (int(joints[25][0]),int(joints[25][1])), 6, (255,0,0), thickness=-1, lineType=8, shift=0) 
	cv2.circle(joint_image, (int(joints[25][0]),int(joints[25][1])), 4, (0,0,255), thickness=-1, lineType=8, shift=0) 
	cv2.circle(joint_image, (int(joints[25][0]),int(joints[25][1])), 2, (255,0,0), thickness=-1, lineType=8, shift=0) 

	
	# 1: 49 # 3: 51 # 5: 53 # 7: 55 # 0: 48
	cv2.namedWindow('joints',cv2.WINDOW_NORMAL)
	while(1):
		print("classify image as either (1)high, (3)medium, (5)mild, (7)low, or (0)zero")
		print("  (1)high:   brandished pistol, aimed position, discharge imminent")
		print("  (3)medium: weapon drawn from holster, but not held in firing position")
		print("  (5)mild:   pistol is holstered, but hand is near or touching the weapon (quickdraw)")
		print("  (7)low:    pistol is present in the frame, but the hands of the individual is not near a drawing position")
		print("  (0)zero:   pistol is erroneously associated with skeleton, or skeleton is poorly formed such that the association is bad")
		cv2.imshow('joints',joint_image)
		cv2.resizeWindow('joints', joint_image.shape[0]*4,joint_image.shape[0]*4)
		k = cv2.waitKey(0)
		if k==122: # Esc key to stop
			threat = 0
			break
		if k==49: # 1 = high
			threat = 1
			break
		if k==51: # 3 = medium
			threat = 3
			break
		if k==53: # 5 = mild
			threat = 5
			break
		if k==55: # 7 = low
			threat = 7
			break
		if k==48: # 0 = zero
			threat = 0
			break
		else:
			print k
	cv2.destroyWindow("joints")
	return threat

def check_pistol_cropped_location(potential_threat, cv_image, crop_image_offset):
	# potential_threat = {
	# 'xmin':person_box['xmin'],
	# 'ymin':person_box['ymin'],
	# 'xmax':person_box['xmax'],
	# 'ymax':person_box['ymax'], 
	# 'pistol_x':pistol_box['center_x']-person_box['xmin'], 
	# 'pistol_y':pistol_box['center_y']-person_box['ymin']
	# }

	if potential_threat['xmin'] < crop_image_offset: 
		x = potential_threat['pistol_x'] + potential_threat['xmin']
	else:
		x = potential_threat['pistol_x'] + crop_image_offset

	if potential_threat['ymin'] < crop_image_offset: 
		y = potential_threat['pistol_y'] + potential_threat['ymin']
	else:
		y = potential_threat['pistol_y'] + crop_image_offset
	return x,y 

def img_crop(image, x_min, x_max, y_min, y_max):
	if (x_min <= 0):
		x_min = 0
	if (y_min <=0 ):
		y_min = 0
	if (x_max >= image.shape[1]):
		x_max = image.shape[1]
	if (y_max >= image.shape[0]):
		y_max = image.shape[0]

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
	print("\n\n\n\n")
	# Setup config
	with open("five_class_dataset.yaml", 'r') as ymlfile:
		if sys.version_info[0] > 2:
			cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
		else:
			cfg = yaml.load(ymlfile)

	print("image_folder:      {}").format(cfg['image_folder'])
	print("label_folder:      {}").format(cfg['label_folder'])
	print("classified_folder: {}").format(cfg['classified_folder'])
	print("subimage_folder:   {}").format(cfg['subimage_folder'])


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

	# image_filename = "aggressive_000302.jpg"
	for image_filename in image_files:
		print("\n\n")
		# load image and labels
		current_image = cfg['image_folder'] + image_filename
		# current_image = cfg['image_folder'] + "aggressive_000302.jpg"
		print("current_image: {}").format(current_image)

		cv_image = cv2.imread(current_image,cv2.IMREAD_COLOR) #load image in cv2
		cv_img_height = cv_image.shape[0]
		cv_img_width = cv_image.shape[1]
		# print("{}, (w,h): ({},{})").format(current_image, cv_img_width, cv_img_height)

		# load bounding boxes from labels
		person_boxes = []
		pistol_boxes = []
		label_file = cfg['label_folder']+image_filename[:-4]+".txt"
		print("label file: {}").format(label_file)
		with open(label_file) as file:
			for line in file: 
				line = line.strip().split() #or some other preprocessing
				# print("line: {}").format(line)
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
					pistol_boxes.append({
						'xmin':x_min,
						'ymin':y_min,
						'xmax':x_max,
						'ymax':y_max, 
						'center_x':box_center_x, 
						'center_y':box_center_y
						})
				if line[0] == "1": # then it is a person
					person_boxes.append({'xmin':x_min,'ymin':y_min,'xmax':x_max,'ymax':y_max})
		
		# print("person_boxes: {}").format(person_boxes)
		# print("pistol_boxes: {}").format(pistol_boxes)

		# check overlapping boxes & associate pistols with people
		for (dirpath, dirnames, filenames) in walk(cfg['subimage_folder']+'high/images/'):
			number_highs = len(filenames)
			break
		for (dirpath, dirnames, filenames) in walk(cfg['subimage_folder']+'medium/images/'):
			number_meds = len(filenames)
			break
		for (dirpath, dirnames, filenames) in walk(cfg['subimage_folder']+'mild/images/'):
			number_milds = len(filenames)
			break
		for (dirpath, dirnames, filenames) in walk(cfg['subimage_folder']+'low/images/'):
			number_lows = len(filenames)
			break
		for (dirpath, dirnames, filenames) in walk(cfg['subimage_folder']+'zero/images/'):
			number_zeros = len(filenames)
			break
		# print("number of (high, medium, low, zero) subimages: ({}, {}, {}, {})").format(number_highs, number_meds, number_lows, number_zeros)

		potential_threats = []
		for person_box in person_boxes:
			for pistol_box in pistol_boxes:
				# if pistol is associated, 
				if box_overlap(person_box, pistol_box):
					potential_threat = {
						'xmin':person_box['xmin'],
						'ymin':person_box['ymin'],
						'xmax':person_box['xmax'],
						'ymax':person_box['ymax'], 
						'pistol_x':pistol_box['center_x']-person_box['xmin'], 
						'pistol_y':pistol_box['center_y']-person_box['ymin']
						}
					potential_threat['pistol_x'], potential_threat['pistol_y'] = check_pistol_cropped_location(potential_threat, cv_image, cfg['crop_image_offset'])
					potential_threats.append(potential_threat)
					
		for potential_threat in potential_threats:
			# print("potential_threat: {}").format(potential_threat)
			# print("potential_threat['xmin']: {}").format(potential_threat['xmin'])
			# create raw sub image, 
			cropped = img_crop(cv_image, 
				potential_threat['xmin']-cfg['crop_image_offset'], 
				potential_threat['xmax']+cfg['crop_image_offset'], 
				potential_threat['ymin']-cfg['crop_image_offset'], 
				potential_threat['ymax']+cfg['crop_image_offset'])
			# cv2.namedWindow('cropped',cv2.WINDOW_NORMAL)
			# cv2.imshow("cropped", cropped)
			# cv2.waitKey(0)
			# cv2.destroyWindow("cropped")

			# calculate skeleton
			skel_image = cropped.copy()
			datum.cvInputData = skel_image
			opWrapper.emplaceAndPop([datum])
			skeletons = datum.poseKeypoints

			x = np.empty((1,9,2))
			rele_dexes = [1,2,3,4,5,6,7,9,12]		
			right_elbow = 3
			right_wrist = 4



			if skeletons.size > 1:
				# cv2.namedWindow('skeleton',cv2.WINDOW_NORMAL)
				# cv2.imshow("skeleton", datum.cvOutputData)
				# cv2.resizeWindow('skeleton', datum.cvOutputData.shape[0]*4,datum.cvOutputData.shape[0]*4)

				for joints in skeletons:
					# print("joints: {}").format(joints)
					# print("joints[rele_dexes]: {}").format(joints[rele_dexes])
					if joints[rele_dexes].all():
						# add pistol to skeleton 
						pistol_location = ([potential_threat['pistol_x'], potential_threat['pistol_y'], 0])
						pistol_joints = np.vstack((joints,pistol_location))

						# ask for user input on threat class
						threat_class = show_keypoints_on_image(datum.cvOutputData, pistol_joints)

						if threat_class == 1: # high threat
							print("    threat_class: {}").format("high")
							if cfg['save_skeltons']:
								image_file = ("{0}{1}high_threat_{2:06d}").format(cfg['subimage_folder'], 'high/images/',number_highs)
								skeleton_file = ("{0}{1}high_threat_{2:06d}").format(cfg['subimage_folder'], 'high/skeletons/',number_highs)
								cv2.imwrite(image_file+".jpg", cropped) # save skeleton image
								np.save(skeleton_file+".npy", pistol_joints) # Save numpy arrays
								np.savetxt(skeleton_file+".txt", pistol_joints, delimiter=',', fmt='%4.2f')   # X is an array
							number_highs += 1
						elif threat_class == 3: # medium threat
							print("    threat_class: {}").format("medium")
							if cfg['save_skeltons']:
								image_file = ("{0}{1}medium_threat_{2:06d}").format(cfg['subimage_folder'], 'medium/images/',number_meds)
								skeleton_file = ("{0}{1}medium_threat_{2:06d}").format(cfg['subimage_folder'], 'medium/skeletons/',number_meds)
								cv2.imwrite(image_file+".jpg", cropped) # save skeleton image
								np.save(skeleton_file+".npy", pistol_joints) # Save numpy arrays
								np.savetxt(skeleton_file+".txt", pistol_joints, delimiter=',', fmt='%4.2f')   # X is an array
							number_meds += 1
						elif threat_class == 5: # mild threat
							print("    threat_class: {}").format("mild")
							if cfg['save_skeltons']:
								image_file = ("{0}{1}mild_threat_{2:06d}").format(cfg['subimage_folder'], 'mild/images/',number_milds)
								skeleton_file = ("{0}{1}mild_threat_{2:06d}").format(cfg['subimage_folder'], 'mild/skeletons/',number_milds)
								cv2.imwrite(image_file+".jpg", cropped) # save skeleton image
								np.save(skeleton_file+".npy", pistol_joints) # Save numpy arrays
								np.savetxt(skeleton_file+".txt", pistol_joints, delimiter=',', fmt='%4.2f')   # X is an array
							number_milds += 1
						elif threat_class == 7: # low threat
							print("    threat_class: {}").format("low")
							if cfg['save_skeltons']:
								image_file = ("{0}{1}low_threat_{2:06d}").format(cfg['subimage_folder'], 'low/images/',number_lows)
								skeleton_file = ("{0}{1}low_threat_{2:06d}").format(cfg['subimage_folder'], 'low/skeletons/',number_lows)
								cv2.imwrite(image_file+".jpg", cropped) # save skeleton image
								np.save(skeleton_file+".npy", pistol_joints) # Save numpy arrays
								np.savetxt(skeleton_file+".txt", pistol_joints, delimiter=',', fmt='%4.2f')   # X is an array
							number_lows += 1
						elif threat_class == 0: # zero threat
							print("    threat_class: {}").format("zero")
							if cfg['save_skeltons']:
								image_file = ("{0}{1}zero_threat_{2:06d}").format(cfg['subimage_folder'], 'zero/images/',number_zeros)
								skeleton_file = ("{0}{1}zero_threat_{2:06d}").format(cfg['subimage_folder'], 'zero/skeletons/',number_zeros)
								cv2.imwrite(image_file+".jpg", cropped) # save skeleton image
								np.save(skeleton_file+".npy", pistol_joints) # Save numpy arrays
								np.savetxt(skeleton_file+".txt", pistol_joints, delimiter=',', fmt='%4.2f')   # X is an array
							number_zeros += 1
						else:
							print("should never get here, something weird happened")
						#move original image to sorted folder

						print("      {}").format(skeleton_file)

				# cv2.destroyWindow("skeleton")

		move(current_image, cfg['classified_folder'] + image_filename)


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