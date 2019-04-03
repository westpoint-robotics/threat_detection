import sys; sys.path.append('/usr/local/python')
import cv2
from os import walk # for listing contents of a directory
import argparse
import yaml
import numpy as np
from openpose import pyopenpose as op


with open("cmu_config.yml", 'r') as ymlfile:
    if sys.version_info[0] > 2:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    else:
        cfg = yaml.load(ymlfile)



# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
# params["model_folder"] = "/home/benjamin/CMU/openpose/models/"
params["model_folder"] = cfg['model_folder']
params["model_pose"] = cfg['model_pose']

# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

# Process Image
datum = op.Datum()

# walk 'unique' for renamable list
image_list = []
for (dirpath, dirnames, filenames) in walk(cfg['image_folder']):
    image_list.extend(filenames)
    break


n=0
while image_list:
    n+=1
    # print("{}").format(n)
    current_image = cfg['image_folder']+image_list[0]
    print("current_image = {}".format(current_image[:-4]))

    imageToProcess = cv2.imread(current_image)
    datum.cvInputData = imageToProcess
    opWrapper.emplaceAndPop([datum])

    # Display Image
    # print("Body keypoints: \n" + str(datum.poseKeypoints))
    # print(type(datum.cvOutputData))
    cv2.imshow(image_list[0], datum.cvOutputData)
    np.save(current_image[:-4], datum.cvOutputData)
    cv2.waitKey(250)

    cv2.destroyWindow(image_list[0])
    image_list.remove(image_list[0])

    if n == 3:
        break