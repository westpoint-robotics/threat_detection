import sys
import numpy as np
import cv2
from os import walk # for listing contents of a directory
from shutil import copyfile # for copying duplicates to folder (for now)
from shutil import move # for moving duplicates to folder (eventually)
import random
import yaml
import json

import pickle


def json_load_byteified(file_handle):
	return _byteify(
		json.load(file_handle, object_hook=_byteify),
		ignore_dicts=True
	)

def json_loads_byteified(json_text):
	return _byteify(
		json.loads(json_text, object_hook=_byteify),
		ignore_dicts=True
	)

def _byteify(data, ignore_dicts = False):
	# if this is a unicode string, return its string representation
	if isinstance(data, unicode):
		return data.encode('utf-8')
	# if this is a list of values, return list of byteified values
	if isinstance(data, list):
		return [ _byteify(item, ignore_dicts=True) for item in data ]
	# if this is a dictionary, return dictionary of byteified keys and values
	# but only if we haven't already byteified it
	if isinstance(data, dict) and not ignore_dicts:
		return {
			_byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
			for key, value in data.iteritems()
		}
	# if it's anything else, return it in its original form
	return data

def main():
	print("\n\n\n\n\n\n\n")

	# Setup config
	with open("alphapose_split_json.yaml", 'r') as ymlfile:
		if sys.version_info[0] > 2:
			cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
		else:
			cfg = yaml.load(ymlfile)


	jsondata = json_load_byteified(open(cfg['json_file']))

	json_block_path = cfg['json_blocks']


	n=0
	for entry in jsondata:
		jsontext = ('[\n{{\n"image_id": "{0}", \n"category_id": {1}, \n"keypoints": {2}, \n"score": {3}\n}}\n]').format(entry["image_id"], entry["category_id"], entry["keypoints"], entry["score"])
		# print(jsontext)
		json_filename = cfg['json_files']+"json_{0:06d}.json".format(n)
		json_file = open(json_filename,"w") 
		json_file.write(jsontext) 
		# print(json_filename)
		json_file.close() 
		n+=1

	# for n in range(0,number_of_blocks):
	# 	# print("block number: {}").format(n)
	# 	block_filename = json_block_path + "json_block_{0:03d}.pkl".format(n)
	# 	print("block filename: {}").format(block_filename)
	# 	json_block = []

	# 	for entry in range(n*block_size, n*block_size+block_size):
	# 		json_block.append(jsondata[entry])
	# 		# print("\n jsondata[{}]: {}").format(entry, jsondata[entry])

	# 	with open(block_filename, 'wb') as handle:
	# 		pickle.dump(json_block, handle, protocol=pickle.HIGHEST_PROTOCOL)
	


if __name__ == "__main__":
	main()

