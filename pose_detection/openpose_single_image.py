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
		print("    joints: {}").format(joints)
		print("      last joint: {}, {}").format(joints[-1][0], joints[-1][1])
		joint_index = 0
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

cv2.imshow("OpenPose 1.4.0 - Tutorial Python API", opImage)
cv2.waitKey(0)

save_filename = "/home/benjamin/datasets/FullPistol/" + cfg['model_pose'] + "_" + image_filename
print("  save_filename :  {}").format(save_filename)
cv2.imwrite(save_filename, opImage) # save skeleton image
