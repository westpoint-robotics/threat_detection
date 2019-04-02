# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
from os import walk # for listing contents of a directory
import argparse
import yaml

sys.path.append('/usr/local/python')
from openpose import pyopenpose as op
# dir_path = os.path.dirname(os.path.realpath(__file__))



def main():
    with open("cmu_config.yml", 'r') as ymlfile:
        if sys.version_info[0] > 2:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        else:
            cfg = yaml.load(ymlfile)

    # Flags
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--image_path", default="/home/benjamin/pipelineOP/examples/media/COCO_val2014_000000000192.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    # args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "/home/benjamin/CMU/openpose/models/"

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
        current_image = cfg['image_folder']+image_list[0]
        print("current_image = {}".format(current_image))

        imageToProcess = cv2.imread(current_image)
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop([datum])

        # Display Image
        print("Body keypoints: \n" + str(datum.poseKeypoints))
        cv2.imshow(image_list[0], datum.cvOutputData)
        cv2.waitKey(0)

        cv2.destroyWindow(image_list[0])
        image_list.remove(image_list[0])


if __name__ == "__main__":
    main()
