import sys
import cv2
import numpy as np
from os import walk # for listing contents of a directory
from os import mkdir # for making directories of possible duplicates
from shutil import copyfile # for copying duplicates to folder (for now)
from shutil import move # for moving duplicates to folder (eventually)
from skimage.measure import compare_ssim as ssim # from skimage.measure import structural_similarity as ssim
import time
import yaml
import matplotlib.pyplot as plt
from uH_lib import * # my libraries


def main():
    with open("uh_config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    estimation_thresh = cfg.get('estimation_threshhold')
    if estimation_thresh is None:
        estimation_thresh = 0.65

    break_threshhold = cfg.get('break_threshhold')
    if break_threshhold is None:
        break_threshhold = 0.65


    print("   ")
    print("Estimation Threshold: {}").format(estimation_thresh)
    print("Break Threshold: {}").format(break_threshhold)
    print("checking: {} ").format(cfg['check_images'])
    print("against:  {} ").format(cfg['uniques_path'])
    print("   ")


    # walk 'unsorted' for new_image list
    unsorted_list = []
    for (dirpath, dirnames, filenames) in walk(cfg['check_images']):
        unsorted_list.extend(filenames)
        break

    init_time = time.time()
    k=0 # number of new images checked
    acc=0 # accumulating time for processing images

    while unsorted_list:
        ts = time.gmtime()
        start_time = time.time()
        tempimg = readImage(cfg['check_images']+ unsorted_list[0])
        print("   ")
        print("{} remaining images in {}").format(len(unsorted_list), cfg['check_images'])
        print("   checking image: {} , [h,w] = [{} {}]").format(unsorted_list[0], tempimg.shape[0], tempimg.shape[1])
        # init/zero variable
        ratio_by_dir = []
        list_of_dirs = []
        dir_index = 0
        folder_ssID = 0
        best_image_match = None

        dupes_folders = []
        for (dirpath, dirnames, filenames) in walk(cfg['possible_dupes_root']):
            dupes_folders.extend(dirnames)
            break

        for dupeset in dupes_folders:
            folder_ssID, best_image_match = compare_ssID_against_folder(cfg['check_images']+unsorted_list[0], cfg['possible_dupes_root']+dupeset+"/")
            list_of_dirs.append(cfg['possible_dupes_root']+dupeset)
            ratio_by_dir.append(folder_ssID)

        if (folder_ssID<break_threshhold):
            unique_ssID, unique_image_match = compare_ssID_against_folder(cfg['check_images']+unsorted_list[0],cfg['uniques_path'])

        if not ratio_by_dir:
            ratio_by_dir = [0,0]

        if ((max(ratio_by_dir)<estimation_thresh) and (unique_ssID<estimation_thresh)) :
            print("  No match found for " + cfg['check_images']+unsorted_list[0])
            # add current image to unique folder
            # print('    move('+ cfg['check_images'] + unsorted_list[0]+ ', ' + cfg['uniques_path']+unsorted_list[0] + ')')
            move(cfg['check_images'] + unsorted_list[0], cfg['uniques_path']+unsorted_list[0])
            new_path = cfg['uniques_path']
        else: # at least one is above the threshold
            if (max(ratio_by_dir)>unique_ssID): 
                # then move to correct dupe folder
                # print('  move(' + cfg['check_images']+unsorted_list[0] + ', ' + list_of_dirs[ratio_by_dir.index(max(ratio_by_dir))]+ '/' +unsorted_list[0] + ')')
                print('  match found in ' + list_of_dirs[ratio_by_dir.index(max(ratio_by_dir))])
                move(cfg['check_images']+unsorted_list[0],list_of_dirs[ratio_by_dir.index(max(ratio_by_dir))]+ '/' +unsorted_list[0])
                new_path = list_of_dirs[ratio_by_dir.index(max(ratio_by_dir))]
            else:
                print('  match found in ' + cfg['uniques_path'])
                # make new dupe folder with old unique and new check image
                newdir = cfg['possible_dupes_root']+'set'+str(len(dupes_folders)+1) 
                # print('mkdir(' + newdir  + ')' )
                mkdir(newdir)
                # print('  move(' + cfg['check_images']+unsorted_list[0] + ', ' + newdir + '/' + unsorted_list[0] + ')')
                move(cfg['check_images']+unsorted_list[0], newdir + '/' + unsorted_list[0])
                move(cfg['uniques_path']+unique_image_match, newdir + '/' + unique_image_match)
                new_path = newdir

                # unique_image_match

        uniques_list = []
        for (dirpath, dirnames, filenames) in walk(cfg['uniques_path']):
            uniques_list.extend(filenames)
            break
        num_uniques = len(uniques_list)
        # print("  Compared " + unsorted_list[0] + " against " + str(num_uniques) + " images")
        print("  Image moved to {}").format(new_path)
        print("    total time: {} minutes").format((time.time() - start_time)/60)
        print("    avg per image: {} seconds").format((time.time() - start_time)/num_uniques)
        k+=1
        acc+=(time.time() - start_time)/60
        # print("  Sorted " + str(k) + " new images, on average each image required " + str(acc/k) + " minutes")
        print("  Sorted {} new images, on average each image required {} minutes").format(k, acc/k)
        # print ('unsorted_list.remove(' + unsorted_list[0] + ')') 
        unsorted_list.remove(unsorted_list[0]) # remove current image from unsorted list

if __name__ == "__main__":
    main()
