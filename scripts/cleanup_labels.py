#!/bin/python
import sys
from os import walk # for listing contents of a directory
# from shutil import move # for moving label files
import shutil as sh
import yaml
import cv2
from uH_lib import * # my libraries

def main():
	print(" ")
	with open("cleanup_labels.yaml", 'r') as ymlfile:
		cfg = yaml.load(ymlfile)

	print("image_path: {}").format(cfg['image_path'])
	print("label_path: {}").format(cfg['label_path'])
	print("label_dest: {}").format(cfg['label_dest'])

	# walk source folder for renamable list
	image_list = []
	for (dirpath, dirnames, filenames) in walk(cfg['image_path']):
		image_list.extend(filenames)
		break

	n=0
	while image_list:
		n+=1
		current_image = image_list[0]
		current_name = current_image[7:-4]+'.txt'
		print("  move({},  {})").format(cfg['label_path']+current_name, cfg['label_dest'])

		try:
			sh.move(cfg['label_path']+current_name, cfg['label_dest'])
		except sh.Error as err:
			print("OS error: {0}".format(err))
		except:
			print("Unexpected error:", sys.exc_info()[0])

		image_list.remove(image_list[0])

if __name__ == "__main__":
	main()
