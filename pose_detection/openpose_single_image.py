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

with open("yolo_config.yml", 'r') as ymlfile:
    if sys.version_info[0] > 2:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    else:
        cfg = yaml.load(ymlfile)

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
datum.cvInputData = imageToProcess
opWrapper.emplaceAndPop([datum])

# Display Image
# print("Body keypoints: \n" + str(datum.poseKeypoints))
# np.save(imagename[:-4], datum.poseKeypoints)

cv2.imshow("OpenPose 1.4.0 - Tutorial Python API", datum.cvOutputData)
cv2.waitKey(0)
