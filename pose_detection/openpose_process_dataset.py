# From Python
# It requires OpenCV installed for Python
import sys; sys.path.append('/usr/local/python')
import cv2
from os import walk # for listing contents of a directory
import argparse
import yaml
import numpy as np
from openpose import pyopenpose as op


def main():
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

    images_processed = 0
    for image in image_list:
        current_image = cfg['image_folder']+image
        keypoint_file = cfg['keypoint_folder']+image[:-4]
        output_file = cfg['output_folder']+image
        # print("output_file = {}".format(output_file))
        # print("current_image = {}".format(current_image))

        imageToProcess = cv2.imread(current_image)
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop([datum])

        # Save numpy arrays
        if cfg['save_keypoints']:
            # print("Body keypoints: \n" + str(datum.poseKeypoints))
            # print(type(datum.cvOutputData))
            np.save(keypoint_file, datum.poseKeypoints)

        # Display Image
        if cfg['show_images']:
            cv2.imshow(image, datum.cvOutputData)
            cv2.waitKey(0)
            cv2.destroyWindow(image)

        if cfg['save_output_image']:
            cv2.imwrite(output_file,datum.cvOutputData)

        images_processed += 1
        if images_processed%100 == 0:
            print("\n    Images to process remaining in {} : {} \n").format(cfg['image_folder'], len(image_list)-images_processed)

if __name__ == "__main__":
    main()


# 
