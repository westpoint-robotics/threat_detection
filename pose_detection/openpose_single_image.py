# From Python
# It requires OpenCV installed for Python
import sys; sys.path.append('/usr/local/python')
import cv2
import os
from sys import platform
import argparse
import yaml
from openpose import pyopenpose as op
import numpy as np

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
	(0,1), (1,8), (8,9), (8,12), #torso
	(1,2), (2,3), (3,4), #right arm
	(1,5), (5,6), (6,7)] #left arm

	for pair in pairs:
		try:
			cv2.line(image, (int(joints[pair[0]][0]), int(joints[pair[0]][1])), (int(joints[pair[1]][0]), int(joints[pair[1]][1])), (0,255,0), thickness=1, lineType=8, shift=0) 
		except:
			print("Joint missing from bone")
		
	return image


def main():
	print("\n\n\n\n\n\n\n")

	with open("openpose_single_image.yaml", 'r') as ymlfile:
			if sys.version_info[0] > 2:
					cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
			else:
					cfg = yaml.load(ymlfile)

	# text params
	fontFace = cv2.FONT_HERSHEY_DUPLEX
	text_color = (0,0,0)
	fontScale = 1
	text_thickness = 1


	# Custom Params (refer to include/openpose/flags.hpp for more parameters)
	params = dict()
	params["model_folder"] = cfg['model_folder']
	params["model_pose"] = cfg['model_pose']

	# Starting OpenPose
	opWrapper = op.WrapperPython()
	opWrapper.configure(params)
	opWrapper.start()

	# Process Image
	datum = op.Datum()
	imageToProcess = cv2.imread(cfg['single_image'])
	path_strings = cfg['single_image'].split('/')
	image_filename = path_strings[-1]
	print("   image file:  {}").format(image_filename)
	datum.cvInputData = imageToProcess
	opWrapper.emplaceAndPop([datum])

	skeletons = datum.poseKeypoints
	opImage = datum.cvOutputData

	if skeletons.size > 1:
		for joints in skeletons:
			# print("    joints: {}").format(joints)
			i = 0
			for joint in joints:
				print("joint #{}, (x,y) : ({}, {}), confidence: {}").format(i, joint[0], joint[1], joint[2])
				i += 1
			# print("      last joint: {}, {}").format(joints[-1][0], joints[-1][1])
			joint_index = 0
			keypoint_image = show_keypoints_on_image(imageToProcess, joints)
			for joint in joints: 
				# print("   joint_index: {}").format(joint_index)
				# print("   fontFace: {}").format(fontFace)
				# print("   fontScale: {}").format(fontScale)
				# print("   text_thickness: {}").format(text_thickness)
				textSize = cv2.getTextSize(str(joint_index), fontFace, fontScale, text_thickness);
				text_width = textSize[0][0]
				text_height = textSize[0][1]
				text_baseline = textSize[1]
				cv2.putText(opImage,str(joint_index),(int(joint[0]),int(joint[1])), fontFace, fontScale, text_color,text_thickness,cv2.LINE_AA)


				joint_index += 1


	# Display Image
	# print("Body keypoints: \n" + str(datum.poseKeypoints))
	# np.save(imagename[:-4], datum.poseKeypoints)

	# cv2.imshow(image_filename, opImage)
	# cv2.waitKey(0)

	save_filename = "/home/benjamin/datasets/rick_body25.png"
	print("  save_filename :  {}").format(save_filename)
	cv2.imwrite(save_filename, keypoint_image) # save skeleton image


if __name__ == "__main__":
	main()