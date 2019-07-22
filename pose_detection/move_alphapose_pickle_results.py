import sys
import numpy as np
import cv2
import os # for testing paths
from os import walk # for listing contents of a directory
from shutil import copyfile # for copying duplicates to folder (for now)
from shutil import move # for moving duplicates to folder (eventually)
import random
import yaml
import json
import pickle

def main():
	print("\n\n\n\n\n\n\n")

	# Setup config
	with open("move_alphapose.yaml", 'r') as ymlfile:
		if sys.version_info[0] > 2:
			cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
		else:
			cfg = yaml.load(ymlfile)

	# list of pickle folders
	pickle_root = cfg['pickle_blocks']
	skeleton_root = cfg['skeleton_root']
	threat_order = ["1_high", "2_medium", "3_mild", "4_low"]
	threat_prefix = ["high_threat", "medium_threat", "mild_threat", "low_threat"]
	number_of_bulk_skeletons = [0,0,0,0]
	
	# print("{}").format(pickle_root)
	for (dirpath, dirnames, pickle_files) in walk(pickle_root):
		break

	# pickle_folder = ("{}json_block_000/skeletons/").format(pickle_root)
	for pickle_dir in dirnames:
		# for each pickle folder, move each H/M/m/L skeletons
		pickle_folder = ("{}{}/skeletons/").format(pickle_root, pickle_dir)
		pickle_images = ("{}{}/images/").format(pickle_root, pickle_dir)
		# print("{}{}/").format(pickle_root, pickle_dir)
		# print("{}").format(pickle_folder)
		for (dirpath, threat_dirs, filenames) in walk(pickle_folder):
			break
	
		for threat_index in range(0,len(threat_order)):
			threat_folder = ("{}{}/").format(pickle_folder, threat_order[threat_index])
			bulk_destination = ("{}{}/").format(skeleton_root, threat_order[threat_index])
			# print(" \n\n ")
			# print("     threat_folder: {}").format(threat_folder)
			# print("  bulk_destination: {}").format(bulk_destination)
			image_folder = ("{}{}/").format(pickle_images, threat_order[threat_index])
			images_destination = ("{}{}/images/").format(skeleton_root, threat_order[threat_index])
			# print("      image_folder: {}").format(image_folder)
			# print("images_destination: {}").format(images_destination)
			for (dirpath, dirnames, skeleton_files) in walk(threat_folder):
				break
			number_of_skeletons = len(skeleton_files)/2
			for skeleton_index in range(0,number_of_skeletons):
				current_name = ("{0}{1}_{2:03d}.npy").format(threat_folder, threat_prefix[threat_index], skeleton_index)
				new_name = ("{0}skeletons/{1}_{2:03d}.npy").format(bulk_destination, threat_prefix[threat_index], number_of_bulk_skeletons[threat_index])
				# print("current_name:  {0}").format(current_name)
				# print("new_name    :  {0}").format(new_name)
				copyfile(current_name, new_name) 
				current_name = ("{0}{1}_{2:03d}.txt").format(threat_folder, threat_prefix[threat_index], skeleton_index)
				new_name = ("{0}skeletons/{1}_{2:03d}.txt").format(bulk_destination, threat_prefix[threat_index], number_of_bulk_skeletons[threat_index])
				# print("current_name:  {0}").format(current_name)
				# print("new_name    :  {0}").format(new_name)
				copyfile(current_name, new_name) 
				current_name = ("{0}{1}_{2:03d}.jpg").format(image_folder, threat_prefix[threat_index], skeleton_index)
				new_name = ("{0}{1}_{2:03d}.jpg").format(images_destination, threat_prefix[threat_index], number_of_bulk_skeletons[threat_index])
				# print("current_name:  {0}").format(current_name)
				# print("new_name    :  {0}").format(new_name)
				copyfile(current_name, new_name) 

				number_of_bulk_skeletons[threat_index]+=1

		

		# print("{0}_{1:03d}.txt").format(threat_prefix[threat_index], skeleton_index)
		# copy and rename files


        # current_name = cfg['original_path']+unnamed_list[0]
        # new_name = cfg['renamed_path']+cfg['renamed_prefix']+str(n).zfill(6)+'.jpg'
        # # print("  renaming " + current_name)
        # # print("   as ")
        # print("  " + new_name)
        # copyfile(current_name, new_name) 


	# for threat_index in range(0,len(threat_order)):
	# 	threat_folder = ("{}{}/").format(pickle_folder, threat_order[threat_index])
	# 	print("{}").format(threat_folder)

	# pickle_file = pickle_files[0]
	
	# for pickle_file in pickle_files:
	# 	# print("Do you want to keep going?")

	# 	print("processing block: {}").format(pickle_file)
	# 	# check to see if block has been processed before
	# 	if not os.path.isdir(cfg['pickle_blocks']+ pickle_file[:-4]):# then the block has not been processed yet
	# 		if not keep_going():
	# 			return
	# 		os.mkdir(cfg['pickle_blocks']+ pickle_file[:-4])
	# 		os.mkdir(cfg['pickle_blocks']+ pickle_file[:-4]+"/skeletons/")
	# 		os.mkdir(cfg['pickle_blocks']+ pickle_file[:-4]+"/skeletons/1_high")
	# 		os.mkdir(cfg['pickle_blocks']+ pickle_file[:-4]+"/skeletons/2_medium")
	# 		os.mkdir(cfg['pickle_blocks']+ pickle_file[:-4]+"/skeletons/3_mild")
	# 		os.mkdir(cfg['pickle_blocks']+ pickle_file[:-4]+"/skeletons/4_low")
	# 		os.mkdir(cfg['pickle_blocks']+ pickle_file[:-4]+"/skeletons/5_zero")
	# 		os.mkdir(cfg['pickle_blocks']+ pickle_file[:-4]+"/images/")
	# 		os.mkdir(cfg['pickle_blocks']+ pickle_file[:-4]+"/images/1_high")
	# 		os.mkdir(cfg['pickle_blocks']+ pickle_file[:-4]+"/images/2_medium")
	# 		os.mkdir(cfg['pickle_blocks']+ pickle_file[:-4]+"/images/3_mild")
	# 		os.mkdir(cfg['pickle_blocks']+ pickle_file[:-4]+"/images/4_low")
	# 		os.mkdir(cfg['pickle_blocks']+ pickle_file[:-4]+"/images/5_zero")

	# 		with open(cfg['json_blocks']+ pickle_file, 'rb') as handle:
	# 			json_block = pickle.load(handle)

	# 		number_high = 0
	# 		number_med = 0
	# 		number_mild = 0
	# 		number_low = 0
	# 		number_zero = 0

	# 		for entry in json_block:
	# 			print("\n\n\n").format(entry)
	# 			# print("\n   entry: {}").format(entry)

	# 			image_filename = entry['image_id']
	# 			current_image = cfg['src_images'] + image_filename
	# 			print("pickle_file:    {}").format(pickle_file)
	# 			print("current_image:  {}").format(current_image)
	# 			cv_image = cv2.imread(current_image,cv2.IMREAD_COLOR) #load image in cv2
	# 			cv_img_height = cv_image.shape[0]
	# 			cv_img_width = cv_image.shape[1]

	# 			label_file = cfg['label_folder']+image_filename[:-4]+".txt"
	# 			print("label file:     {}").format(label_file)
	# 			pistol_boxes = []



if __name__ == "__main__":
	main()

