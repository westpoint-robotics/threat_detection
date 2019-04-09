import shutil
import numpy as np
import cv2
import os,sys
import time

sys.path.append('/usr/local/python') # path for CMUopenpose library
sys.path.append(os.environ['DARKNET_PATH']) 
sys.path.append(os.environ['DARKNET_PATH']+'/python')

import darknet as dn

yolo_config = '/home/benjamin/ros/src/usma_threat_ros/yolo/pistol-tiny.cfg'
yolo_weights = '/home/benjamin/ros/src/usma_threat_ros/yolo/pistol-tiny_300000.weights'
net = dn.load_net(yolo_config,yolo_weights,0)

yolo_data = '/home/benjamin/ros/src/usma_threat_ros/yolo/pistol.data'
meta = dn.load_meta(yolo_data)

# src_folder = '/home/benjamin/datasets/test/'
src_folder = '/home/benjamin/datasets/test/low_aggressive_000005.jpg'


img = cv2.imread(src_folder,cv2.IMREAD_COLOR) #load image in cv2
objects = dn.detect(net, meta, src_folder)


for detection in objects:
	box_color = (0,255,0)
	center_x = detection[2][0]
	center_y = detection[2][2]
	width = detection[2][1]
	height = detection[2][3]
	UL_x = int(center_x - width/2) #Upper Left corner X coord
	UL_y = int(center_y + height/2) #Upper left Y
	LR_x = int(center_x + width/2)
	LR_y = int(center_y - height/2)
	#write bounding box to image
	cv2.rectangle(img,(UL_x,UL_y),(LR_x,LR_y),box_color,5)
	# cv2.resizeWindow("image", crop_img.shape[0]*1,crop_img.shape[1]*1)
	
cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyWindow("image")




# print("person_box[{}], xmin:[{}], xmax:[{}], ymin:[{}], ymax:[{}] ").format(i, person_box["xmin"], person_box["xmax"], person_box["ymin"], person_box["ymax"]) 
# crop_img = self.cv_image[person_box["ymin"]:person_box["ymax"],  person_box["xmin"]:person_box["xmax"]]


# while True:
#    files = os.listdir(src_folder)
#    #dn.detect fails occasionally. I suspect a race condition.
#    time.sleep(5)
#    for f in files:
#        if f.endswith(".jpg"):
#            print (f)
#            path = os.path.join(src_folder, f)
#            pathb = path.encode('utf-8')
#            res = dn.detect(net, meta, pathb)
#            print (res) #list of name, probability, bounding box center x, center y, width, height
#            i=0
#            new_path = '/home/myusername/Pictures/none/'+f #initialized to none
#            img = cv2.imread(path,cv2.IMREAD_COLOR) #load image in cv2
#            while i<len(res):
#                res_type = res[i][0].decode('utf-8')      
#                if "person" in res_type:
#                    #copy file to person directory
#                    new_path = '/home/myusername/Pictures/person_'+f
#                    #set the color for the person bounding box
#                    box_color = (0,255,0)
#                elif "pistol" in res_type:
#                    new_path = '/home/myusername/Pictures/pistol_'+f
#                    box_color = (0,0,255)
#                #get bounding box
#                center_x=int(res[i][2][0])
#                center_y=int(res[i][2][1])
#                width = int(res[i][2][2])
#                height = int(res[i][2][3])
               
#                UL_x = int(center_x - width/2) #Upper Left corner X coord
#                UL_y = int(center_y + height/2) #Upper left Y
#                LR_x = int(center_x + width/2)
#                LR_y = int(center_y - height/2)
               
#                #write bounding box to image
#                cv2.rectangle(img,(UL_x,UL_y),(LR_x,LR_y),box_color,5)
#                #put label on bounding box
#                font = cv2.FONT_HERSHEY_SIMPLEX
#                cv2.putText(img,res_type,(center_x,center_y),font,2,box_color,2,cv2.LINE_AA)
#                i=i+1
#            cv2.imwrite(new_path,img) #wait until all the objects are marked and then write out.
#            #todo. This will end up being put in the last path that was found if there were multiple
#            #it would be good to put it all the paths.
#            os.remove(path) #remove the original
           
#         