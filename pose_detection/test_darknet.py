import os,sys
import time

sys.path.append('/usr/local/python')
sys.path.append('/home/benjamin/ros/src/darknet_ros/darknet/python')
sys.path.append('/home/benjamin/ros/src/darknet_ros/darknet')

import darknet as dn
import pdb
import shutil
import numpy as np
import cv2


yolocfg = '/home/benjamin/ros/src/usma_threat_ros/cfg/models/pistol-yolov3-tiny.cfg'
yolowts = '/home/benjamin/ros/src/usma_threat_ros/cfg/weights/pistol-yolov3-tiny_last.weights'
yolometa = '/home/benjamin/ros/src/usma_threat_ros/cfg/meta/pistol_obj.data'

# net = cv2.dnn.readNetFromDarknet(yolocfg, yolowts)

net = dn.load_net(yolocfg,yolowts,0)
meta = dn.load_meta(yolometa)

folder = '/home/benjamin/datasets/test/'

while True:
   files = os.listdir(folder)
   #dn.detect fails occasionally. I suspect a race condition.
   time.sleep(5)
   for f in files:
       if f.endswith(".jpg"):
           print (f)
           path = os.path.join(folder, f)
           pathb = path.encode('utf-8')
           res = dn.detect(net, meta, pathb)
           print (res) #list of name, probability, bounding box center x, center y, width, height
           i=0
           new_path = '/home/myusername/Pictures/none/'+f #initialized to none
           img = cv2.imread(path,cv2.IMREAD_COLOR) #load image in cv2
           while i<len(res):
               res_type = res[i][0].decode('utf-8')      
               if "person" in res_type:
                   #copy file to person directory
                   new_path = '/home/myusername/Pictures/people/'+f
                   #set the color for the person bounding box
                   box_color = (0,255,0)
               elif "cat" in res_type:
                   new_path = '/home/myusername/Pictures/cat/'+f
                   box_color = (0,255,255)
               elif "bird" in res_type:
                   new_path = '/home/myusername/Pictures/bird/'+f
                   box_color = (255,0,0)
               elif "squirrel" in res_type:
                   new_path = '/home/myusername/Pictures/squirrel/'+f
                   box_color = (0,0,255)
               #get bounding box
               center_x=int(res[i][2][0])
               center_y=int(res[i][2][1])
               width = int(res[i][2][2])
               height = int(res[i][2][3])
               
               UL_x = int(center_x - width/2) #Upper Left corner X coord
               UL_y = int(center_y + height/2) #Upper left Y
               LR_x = int(center_x + width/2)
               LR_y = int(center_y - height/2)
               
               #write bounding box to image
               cv2.rectangle(img,(UL_x,UL_y),(LR_x,LR_y),box_color,5)
               #put label on bounding box
               font = cv2.FONT_HERSHEY_SIMPLEX
               cv2.putText(img,res_type,(center_x,center_y),font,2,box_color,2,cv2.LINE_AA)
               i=i+1
           cv2.imwrite(new_path,img) #wait until all the objects are marked and then write out.
           #todo. This will end up being put in the last path that was found if there were multiple
           #it would be good to put it all the paths.
           os.remove(path) #remove the original
           
        