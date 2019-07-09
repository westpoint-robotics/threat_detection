import sys
import numpy as np
import cv2
from os import walk # for listing contents of a directory
from shutil import copyfile # for copying duplicates to folder (for now)
from shutil import move # for moving duplicates to folder (eventually)
import random
import yaml
import json

import pickle


def json_load_byteified(file_handle):
	return _byteify(
		json.load(file_handle, object_hook=_byteify),
		ignore_dicts=True
	)

def json_loads_byteified(json_text):
	return _byteify(
		json.loads(json_text, object_hook=_byteify),
		ignore_dicts=True
	)

def _byteify(data, ignore_dicts = False):
	# if this is a unicode string, return its string representation
	if isinstance(data, unicode):
		return data.encode('utf-8')
	# if this is a list of values, return list of byteified values
	if isinstance(data, list):
		return [ _byteify(item, ignore_dicts=True) for item in data ]
	# if this is a dictionary, return dictionary of byteified keys and values
	# but only if we haven't already byteified it
	if isinstance(data, dict) and not ignore_dicts:
		return {
			_byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
			for key, value in data.iteritems()
		}
	# if it's anything else, return it in its original form
	return data


def show_keypoints_on_image(image, joints):
	joint_image = image.copy()
	joint_image = draw_skeleton(image, joints)
	for joint in joints:
		if joint.all():
			# print("joint (x,y): ({}, {})").format(joint[0], joint[1])
			# random joint color
			# cv2.circle(joint_image, (int(joint[0]),int(joint[1])), 4, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), thickness=-1, lineType=8, shift=0) 
			# black joint color with white center
			cv2.circle(joint_image, (int(joint[0]),int(joint[1])), 5, (0,0,0), thickness=-1, lineType=8, shift=0) 
			cv2.circle(joint_image, (int(joint[0]),int(joint[1])), 2, (255,255,255), thickness=-1, lineType=8, shift=0) 

	# cv2.circle(joint_image, (int(joints[-1][0]),int(joints[-1][1])), 8, (0,0,255), thickness=-1, lineType=8, shift=0) 
	# cv2.circle(joint_image, (int(joints[-1][0]),int(joints[-1][1])), 6, (255,0,0), thickness=-1, lineType=8, shift=0) 
	# cv2.circle(joint_image, (int(joints[-1][0]),int(joints[-1][1])), 4, (0,0,255), thickness=-1, lineType=8, shift=0) 
	# cv2.circle(joint_image, (int(joints[-1][0]),int(joints[-1][1])), 2, (255,0,0), thickness=-1, lineType=8, shift=0) 

	
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
	return joint_image

def draw_skeleton(image, joints):
	pairs = [\
	# (0,1), # right shin
	# (1,2), # right thigh
	(2,6), # right hip
	(6,3), # left hip
	# (3,4), # left thigh
	# (4,5), # left shin
	(6,7), # spine
	(7,8), # neck
	(8,9), # head
	(8,12), #right shoulder
	(12,11), #right bicep
	(11,10), #right forearm
	# (10,16), #right gun
	(8,13), #left shoulder
	(13,14), #left bicep
	(14,15)] #left forearm

	for pair in pairs:
		cv2.line(image, (int(joints[pair[0]][0]), int(joints[pair[0]][1])), (int(joints[pair[1]][0]), int(joints[pair[1]][1])), (0,255,0), thickness=1, lineType=8, shift=0) 
	return image

def main():
	print("\n\n\n\n\n\n\n")

	# Setup config
	with open("alphapose_single_json.yaml", 'r') as ymlfile:
		if sys.version_info[0] > 2:
			cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
		else:
			cfg = yaml.load(ymlfile)


	jsondata = json_load_byteified(open(cfg['json_file']))
	cv_image = cv2.imread(cfg['src_image'] ,cv2.IMREAD_COLOR) #load image in cv2

	# print("jsondata : {}").format(jsondata)
	print("jsondata[0]['image_id'] : {}").format(jsondata[0]['image_id'])
	# print("jsondata[0]['category_id'] : {}").format(jsondata[0]['category_id'])
	# print("jsondata[0]['keypoints'] : {}").format(jsondata[0]['keypoints'])
	# print("jsondata[0]['score'] : {}").format(jsondata[0]['score'])

	joints = np.asarray(jsondata[0]['keypoints'])
	joints = np.reshape(joints, (16, 3))
	jsondata[0]['joints'] = joints

	print("jsondata[0]['joints'] : {}").format(jsondata[0]['joints'])


	keypoint_image = show_keypoints_on_image(cv_image, joints)
	cv2.imwrite(cfg['save_image'], keypoint_image) # save skeleton image

if __name__ == "__main__":
	main()

