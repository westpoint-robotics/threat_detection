# checks one image against all images in a folder
# work in progress
# 
def get_all_ssID_matches_from_folder(img_path, folder_path, thresh):
    from os import walk # for listing contents of a directory
    numIterations = 500
    ssIDmax = 0
    best_image_match = None
    H = None
    img1 = readImage(img_path)
    images_in_folder = []
    ssID_matches = []
    for (dirpath, dirnames, filenames) in walk(folder_path):
        images_in_folder.extend(filenames)
        break
    for image_name in images_in_folder:
        img2 = readImage(folder_path + image_name)
        ssID = 0
        corr_matrix = None
        corr_matrix = get_correspondances(img1, img2)
        H, ssID = ransacSSID(corr_matrix, img1, img2, numIterations)
        if (thresh < ssID):
            ssID_matches.append(image_name)
            print('     Found potential dupe:' + image_name + ', ssID: ' + str(ssID))
    return ssID_matches

# 
# checks one image against all images in a folder
# returns maximum ssID for new image against images in folder
# 
def compare_ssID_against_folder(img_path, folder_path):
    from os import walk # for listing contents of a directory
    numIterations = 500
    ssIDmax = 0
    best_image_match = None
    H = None
    img1 = readImage(img_path)
    images_in_folder = []
    for (dirpath, dirnames, filenames) in walk(folder_path):
        images_in_folder.extend(filenames)
        break
    for image_name in images_in_folder:
        img2 = readImage(folder_path + image_name)
        ssID = 0
        corr_matrix = None
        corr_matrix = get_correspondances(img1, img2)
        H, ssID = ransacSSID(corr_matrix, img1, img2, numIterations)
        if (ssIDmax < ssID):
            ssIDmax = ssID
            best_image_match = image_name
            if (ssIDmax > 0.97):
                break
    return ssIDmax, best_image_match

# 
# Get correspondences between two images
# 
def get_correspondances(img1, img2):
    import numpy as np
    #find features and keypoints
    correspondenceList = []

    kp1, desc1 = findFeatures(img1)
    kp2, desc2 = findFeatures(img2)
    # print "Found keypoints in " + img1name + ": " + str(len(kp1))
    # print "Found keypoints in " + img2name + ": " + str(len(kp2))
    keypoints = [kp1,kp2]
    matches = matchFeatures(kp1, kp2, desc1, desc2, img1, img2)
    for match in matches:
        (x1, y1) = keypoints[0][match.queryIdx].pt
        (x2, y2) = keypoints[1][match.trainIdx].pt
        correspondenceList.append([x1, y1, x2, y2])

    corrs = np.matrix(correspondenceList)
    return corrs


def checkAgainstFolder(setnFolder, testFolder, testImage, matchThreshold):
    from os import walk # for listing contents of a directory
    setn_list = []

    for (dirpath, dirnames, filenames) in walk(setnFolder):
        setn_list.extend(filenames)
        break

    # print("    in checkAgainstFolder:")
    # print("      testFolder: " + testFolder)
    # print("      testImage: " + testImage)
    # print("      setnFolder: " + setnFolder)
    # print("      setnImages:")
    # print(setn_list)

    set_match = False
    for setn_image in setn_list:
        # check current image against already found duplicates
        ref_Image = setnFolder + "/" + setn_image
        test_Image = testFolder + testImage
        # print("     checkUniqueness(" + ref_Image + ", " + test_Image)
        # match = checkUniqueness(ref_Image, test_Image, matchThreshold)
        match = compare_images(ref_Image, test_Image, matchThreshold)
        # match = orbUniqueness(ref_Image, test_Image, matchThreshold)
        # print("        checkUniqueness:" +str(match))
        if (match): #the current image DOES match the current duplicate file
            set_match = match
    return set_match

#
# Read in an image file, errors out if we can't find the file
def readImage(filename):
    import cv2
    import math
    import numpy as np
    img = cv2.imread(filename, 0)
    if img is None:
        print('Invalid image:' + filename)
        return None
    else:
        # downsize images to make matching faster
        h = img.shape[0]
        w = img.shape[1]
        a = h*w
        scale = math.sqrt((10000)/float(a))
        sh = int(math.floor(h*scale))
        sw = int(math.floor(w*scale))
        img2 = cv2.resize(img,(sw,sh), interpolation = cv2.INTER_AREA)
        
        kernel = np.ones((5,5),np.float32)/25
        gausimg = cv2.filter2D(img2,-1,kernel)
        return gausimg


#
# Runs sift algorithm to find features
#
def findFeatures(img):
    # print("Finding Features...")
    # sift = cv2.SIFT()
    import cv2
    sift = cv2.xfeatures2d.SIFT_create()
    keypoints = sift.detect(img, None)
    keypoints, descriptors = sift.compute(img, keypoints)

    # keypoints, descriptors = sift.detectAndCompute(img, None)

    img = cv2.drawKeypoints(img, keypoints, None)
    # cv2.imwrite('sift_keypoints.png', img)

    return keypoints, descriptors

#
# Matches features given a list of keypoints, descriptors, and images
#
def matchFeatures(kp1, kp2, desc1, desc2, img1, img2):
    import cv2
    # print("Matching Features...")
    matcher = cv2.BFMatcher(cv2.NORM_L2, True)
    matches = matcher.match(desc1, desc2)
    # matchImg = drawMatches(img1,kp1,img2,kp2,matches)
    # cv2.imwrite('Matches.png', matchImg)
    return matches


#
# Computers a homography from 4-correspondences
#
def calculateHomography(correspondences):
    # import cv2
    import numpy as np
    #loop through correspondences and create assemble matrix
    aList = []
    for corr in correspondences:
        p1 = np.matrix([corr.item(0), corr.item(1), 1])
        p2 = np.matrix([corr.item(2), corr.item(3), 1])

        a2 = [0, 0, 0, -p2.item(2) * p1.item(0), -p2.item(2) * p1.item(1), -p2.item(2) * p1.item(2),
              p2.item(1) * p1.item(0), p2.item(1) * p1.item(1), p2.item(1) * p1.item(2)]
        a1 = [-p2.item(2) * p1.item(0), -p2.item(2) * p1.item(1), -p2.item(2) * p1.item(2), 0, 0, 0,
              p2.item(0) * p1.item(0), p2.item(0) * p1.item(1), p2.item(0) * p1.item(2)]
        aList.append(a1)
        aList.append(a2)

    matrixA = np.matrix(aList)

    #svd composition
    u, s, v = np.linalg.svd(matrixA)

    #reshape the min singular value into a 3 by 3 matrix
    h = np.reshape(v[8], (3, 3))

    #normalize and now we have h
    h = (1/h.item(8)) * h
    return h

#
#Calculate the geometric distance between estimated points and original points
#
def geometricDistance(correspondence, h):
    import numpy as np

    p1 = np.transpose(np.matrix([correspondence[0].item(0), correspondence[0].item(1), 1]))
    estimatep2 = np.dot(h, p1)
    if (estimatep2.item(2)==0):
        return 10000
    else:
        estimatep2 = (1/estimatep2.item(2))*estimatep2
        p2 = np.transpose(np.matrix([correspondence[0].item(2), correspondence[0].item(3), 1]))
        error = p2 - estimatep2
        return np.linalg.norm(error)

#
#Runs through ransac algorithm, creating homographies from random correspondences
#
def ransac(corr, thresh):
    import random
    import numpy as np
    maxInliers = []
    finalH = None
    for i in range(500):
        #find 4 random points to calculate a homography
        corr1 = corr[random.randrange(0, len(corr))]
        corr2 = corr[random.randrange(0, len(corr))]
        randomFour = np.vstack((corr1, corr2))
        corr3 = corr[random.randrange(0, len(corr))]
        randomFour = np.vstack((randomFour, corr3))
        corr4 = corr[random.randrange(0, len(corr))]
        randomFour = np.vstack((randomFour, corr4))

        #call the homography function on those points
        h = calculateHomography(randomFour)
        inliers = []

        for i in range(len(corr)):
            d = geometricDistance(corr[i], h)
            if d < 5:
                inliers.append(corr[i])

        if len(inliers) > len(maxInliers):
            maxInliers = inliers
            finalH = h
        # print "Corr size: ", len(corr), " NumInliers: ", len(inliers), "Max inliers: ", len(maxInliers)

        if len(maxInliers) > (len(corr)*thresh):
            break
    return finalH, maxInliers

def ransacSSID(corr, img1, img2, numIterations):
    import random
    import cv2
    import numpy as np
    from skimage.measure import compare_ssim as ssim # from skimage.measure import structural_similarity as ssim
    maxSSID = 0
    bestH = None
    # numIterations=500
    finalH = None
    for i in range(numIterations):
        #find 4 random points to calculate a homography
        corr1 = corr[random.randrange(0, len(corr))]
        corr2 = corr[random.randrange(0, len(corr))]
        randomFour = np.vstack((corr1, corr2))
        corr3 = corr[random.randrange(0, len(corr))]
        randomFour = np.vstack((randomFour, corr3))
        corr4 = corr[random.randrange(0, len(corr))]
        randomFour = np.vstack((randomFour, corr4))

        #call the homography function on those points
        h = calculateHomography(randomFour)

        warp1 = cv2.warpPerspective(img1, h, (img2.shape[1], img2.shape[0]))
        ssID = ssim(warp1, img2)
        if ssID > maxSSID:
            finalH = h
            maxSSID = ssID
        
        warp2 = cv2.warpPerspective(img2, h, (img1.shape[1], img1.shape[0]))
        ssID = ssim(warp2, img1)
        if ssID > maxSSID:
            finalH = h
            maxSSID = ssID

    return finalH, maxSSID


# 
# Mean squared error of two images
# 
def compare_images(image1, image2, thresh):
    import cv2
    import numpy as np
    from skimage.measure import compare_ssim as ssim # from skimage.measure import structural_similarity as ssim
    # orig1 = readImage(image1)
    # orig2 = readImage(image2)
    # img1 = cv2.resize(orig1,(80,80), interpolation = cv2.INTER_AREA)
    # img2 = cv2.resize(orig2,(80,80), interpolation = cv2.INTER_AREA)
    
    img1 = readImage(image1)
    img2 = readImage(image2)

    #find features and keypoints
    correspondenceList = []

    kp1, desc1 = findFeatures(img1)
    kp2, desc2 = findFeatures(img2)
    # print "Found keypoints in " + img1name + ": " + str(len(kp1))
    # print "Found keypoints in " + img2name + ": " + str(len(kp2))
    keypoints = [kp1,kp2]
    matches = matchFeatures(kp1, kp2, desc1, desc2, img1, img2)
    for match in matches:
        (x1, y1) = keypoints[0][match.queryIdx].pt
        (x2, y2) = keypoints[1][match.trainIdx].pt
        correspondenceList.append([x1, y1, x2, y2])

    corrs = np.matrix(correspondenceList)

    #run ransac algorithm
    ssID = 0
    numIterations = 500
    finalH, ssID = ransacSSID(corrs, thresh, img1, img2, numIterations)
    if ssID>thresh:
        print("  match = compare_images(" + image1 + ", " + image2 + ", " + str(thresh) +")")
        print("   match found, ssim: " +str(ssID))
        return True
    else:
        # print("    no match, ssim: " +str(ssID))
        return False

def recursiveMatch(original_path, original_list, match_threshold):
    current_list = []
    current_list.append(original_list[0])
    original_list.remove(original_list[0]) # remove current image from unsorted list
    current_index = 0 #this will track which image in the current list is being compared against the original list

    while (len(current_list)>current_index):
        for original_image in original_list:
            match = compare_images(original_path+current_list[current_index], original_path+original_image, match_threshold)
            if (match):
                current_list.append(original_image)
                original_list.remove(original_image)
        current_index+=1

    return current_list, original_list




# This draws matches and optionally a set of inliers in a different color
# Note: I lifted this drawing portion from stackoverflow and adjusted it to my needs because OpenCV 2.4.11 does not
# include the drawMatches function
# def drawMatches(img1, kp1, img2, kp2, matches, inliers = None):
#     # Create a new output image that concatenates the two images together
#     rows1 = img1.shape[0]
#     cols1 = img1.shape[1]
#     rows2 = img2.shape[0]
#     cols2 = img2.shape[1]

#     out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

#     # Place the first image to the left
#     out[:rows1,:cols1,:] = np.dstack([img1, img1, img1])

#     # Place the next image to the right of it
#     out[:rows2,cols1:cols1+cols2,:] = np.dstack([img2, img2, img2])

#     # For each pair of points we have between both images
#     # draw circles, then connect a line between them
#     for mat in matches:

#         # Get the matching keypoints for each of the images
#         img1_idx = mat.queryIdx
#         img2_idx = mat.trainIdx

#         # x - columns, y - rows
#         (x1,y1) = kp1[img1_idx].pt
#         (x2,y2) = kp2[img2_idx].pt

#         inlier = False

#         if inliers is not None:
#             for i in inliers:
#                 if i.item(0) == x1 and i.item(1) == y1 and i.item(2) == x2 and i.item(3) == y2:
#                     inlier = True

#         # Draw a small circle at both co-ordinates
#         cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)
#         cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

#         # Draw a line in between the two points, draw inliers if we have them
#         if inliers is not None and inlier:
#             cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (0, 255, 0), 1)
#         elif inliers is not None:
#             cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (0, 0, 255), 1)

#         if inliers is None:
#             cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)

#     return out