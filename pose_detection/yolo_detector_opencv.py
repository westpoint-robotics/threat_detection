# import libraries
import shutil
import numpy as np
import cv2
import os,sys,time
import yaml

#setup and import darknet-yolo
sys.path.append('/usr/local/python') # path for CMUopenpose library
sys.path.append(os.environ['DARKNET_PATH']) 
sys.path.append(os.environ['DARKNET_PATH']+'/python')
import darknet as dn

def array_to_image(arr):
    arr = arr.transpose(2,0,1)
    c = arr.shape[0]
    h = arr.shape[1]
    w = arr.shape[2]
    arr = (arr/255.0).flatten()
    data = dn.c_array(dn.c_float, arr)
    im = dn.IMAGE(w,h,c,data)
    return im

def detect2(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
    boxes = dn.make_boxes(net)
    probs = dn.make_probs(net)
    num =   dn.num_boxes(net)
    dn.network_detect(net, image, thresh, hier_thresh, nms, boxes, probs)
    res = []
    for j in range(num):
        for i in range(meta.classes):
            if probs[j][i] > 0:
                res.append((meta.names[i], probs[j][i], (boxes[j].x, boxes[j].y, boxes[j].w, boxes[j].h)))
    res = sorted(res, key=lambda x: -x[1])
    dn.free_ptrs(dn.cast(probs, dn.POINTER(dn.c_void_p)), num)
    return res


with open("yolo_config.yml", 'r') as ymlfile:
    if sys.version_info[0] > 2:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    else:
        cfg = yaml.load(ymlfile)

# Setup yolo config
yolo_data = cfg['yolo_data'] 
yolo_config = cfg['yolo_config'] 
yolo_weights = cfg['yolo_weights'] 
test_image = cfg['single_image']


# Darknet
net = dn.load_net(yolo_config, yolo_weights, 0)
meta = dn.load_meta(yolo_data)
r = dn.detect(net, meta, test_image)
print r


# OpenCV
arr = cv2.imread(test_image)
im = array_to_image(arr)
dn.rgbgr_image(im)
r = detect2(net, meta, im)
print r

