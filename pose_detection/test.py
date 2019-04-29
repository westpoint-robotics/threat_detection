
import cv2 
imagefile = "/home/benjamin/datasets/Aggressiveness/High_ordered/images/high_aggressive_000056.jpg"
cv_image = cv2.imread(imagefile ,cv2.IMREAD_COLOR) #load image in cv2

height = cv_image.shape[0]
width = cv_image.shape[1]


