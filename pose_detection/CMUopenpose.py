# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import yaml

sys.path.append('/usr/local/python')
from openpose import pyopenpose as op
# dir_path = os.path.dirname(os.path.realpath(__file__))

with open("cmu_config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--image_path", default="/home/benjamin/pipelineOP/examples/media/COCO_val2014_000000000192.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
args = parser.parse_known_args()

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "/home/benjamin/CMU/openpose/models/"

# I think this just changes the "--key " language into dictionary type formats  (this behavior is defaulted in yaml loading)
# for i in range(0, len(args[1])):
#     curr_item = args[1][i]
#     print("curr_item = args[1][i] = {curr_item}").format()
#     if i != len(args[1])-1: next_item = args[1][i+1]
#     else: next_item = "1"
#     if "--" in curr_item and "--" in next_item:
#         key = curr_item.replace('-','')
#         if key not in params:  params[key] = "1"
#     elif "--" in curr_item and "--" not in next_item:
#         key = curr_item.replace('-','')
#         if key not in params: params[key] = next_item

# Construct it from system arguments
# op.init_argv(args[1])
# oppython = op.OpenposePython()

# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

# Process Image
datum = op.Datum()
imageToProcess = cv2.imread(args[0].image_path)
datum.cvInputData = imageToProcess
opWrapper.emplaceAndPop([datum])

# Display Image
print("Body keypoints: \n" + str(datum.poseKeypoints))
cv2.imshow("OpenPose 1.4.0 - Tutorial Python API", datum.cvOutputData)
cv2.waitKey(0)
