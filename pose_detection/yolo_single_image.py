# import libraries
import numpy as np
import cv2
import os,sys
import yaml

#setup and import darknet-yolo
sys.path.append('/usr/local/python') # path for CMUopenpose library
sys.path.append(os.environ['DARKNET_PATH']) 
sys.path.append(os.environ['DARKNET_PATH']+'/python')
import darknet as dn

def main():
	with open("yolo_config.yml", 'r') as ymlfile:
		if sys.version_info[0] > 2:
			cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
		else:
			cfg = yaml.load(ymlfile)

	# Setup yolo config
	yolo_data = cfg['yolo_data'] 
	yolo_config = cfg['yolo_config'] 
	yolo_weights = cfg['yolo_weights'] 

	net = dn.load_net(yolo_config,yolo_weights,0)
	meta = dn.load_meta(yolo_data)

	img = cv2.imread(cfg['single_image'] ,cv2.IMREAD_COLOR) #load image in cv2
	# objects = dn.detect(net, meta, cfg['single_image']) # from filename
	objects = dn.detect(net, meta, img) #opencv image



	for detection in objects:
		box_color = (0,255,0)
		bounds = detection[2]
		xCoord = int(bounds[0] - bounds[2]/2)
		yCoord = int(bounds[1] - bounds[3]/2)
		xCoord2 = int(bounds[0] + bounds[2]/2)
		yCoord2 = int(bounds[1] + bounds[3]/2)
		upper_left = (xCoord,yCoord)
		lower_right2 = (xCoord2, yCoord2)
		cv2.rectangle(img,upper_left,lower_right2,box_color,2)

	# cv2.imwrite(cfg['yolo_savefile'] ,img)
		
	cv2.imshow("image", img)
	cv2.waitKey(0)
	cv2.destroyWindow("image")

if __name__ == "__main__":
	main()
