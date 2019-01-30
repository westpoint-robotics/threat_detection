#!/bin/python
from os import walk # for listing contents of a directory
from shutil import copyfile
import yaml
import cv2
from uH_lib import * # my libraries

def main():
    print(" ")
    with open("rename_config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    # walk 'unique' for renamable list
    unnamed_list = []
    for (dirpath, dirnames, filenames) in walk(cfg['original_path']):
        unnamed_list.extend(filenames)
        break

    n=0
    while unnamed_list:
        n+=1
        current_name = cfg['original_path']+unnamed_list[0]
        new_name = cfg['renamed_path']+cfg['renamed_prefix']+str(n).zfill(6)+'.jpg'
        # print("  renaming " + current_name)
        # print("   as ")
        print("  " + new_name)
        # copyfile(current_name, new_name) 

        img = cv2.imread(current_name)

        # cv2.imshow('image',img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        cv2.imwrite(new_name,img)
        unnamed_list.remove(unnamed_list[0])


if __name__ == "__main__":
    main()
