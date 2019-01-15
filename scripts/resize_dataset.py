#!/bin/python
from os import walk # for listing contents of a directory
from shutil import copyfile
import yaml
import cv2
import math
import numpy as np

# from uH_lib import * # my libraries

def readImage(filename):
    img = cv2.imread(filename, 0)
    if img is None:
        print('Invalid image:' + filename)
        return None
    else:
        # downsize images to make matching faster
        h = img.shape[0]
        w = img.shape[1]
        a = h*w
        scale = math.sqrt((480000)/float(a))  #(600*800=480000)
        sh = int(math.floor(h*scale))
        sw = int(math.floor(w*scale))
        img2 = cv2.resize(img,(sw,sh), interpolation = cv2.INTER_AREA)
        
        kernel = np.ones((3,3),np.float32)/9
        gausimg = cv2.filter2D(img2,-1,kernel)
        return gausimg

def main():

    with open("resize_datset.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    print("Resizing: {} ").format(cfg['original_path'])
    print("Output dir: {} ").format(cfg['resized_path'])

    original_datasets_path= cfg['original_path']

    # walk 'unique' for renamable list
    original_list = []
    for (dirpath, dirnames, filenames) in walk(original_datasets_path):
        original_list.extend(filenames)
        break

    for image in original_list:
        image_path = cfg['original_path'] + image
        # print("image_path : {}").format(image_path)
        smaller_image = readImage(image_path)
        # print("output image: {}").format(cfg['resized_path'] + image[:-4]+'.jpg')
        cv2.imwrite(cfg['resized_path'] + image[:-4]+'.jpg',smaller_image)

if __name__ == "__main__":
    main()
