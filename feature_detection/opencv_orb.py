import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('depthmap.jpg', 0)
#Orb initialization
orb = cv.ORB_create(nfeatures=10000, scoreType = cv.ORB_FAST_SCORE)
#keypoints
kp = orb.detect(img,None)

kp, des = orb.compute(img, kp)

img2 =cv.drawKeypoints(img, kp, 0,color=(0,255,0), flags = 0)
plt.imshow(img2), plt.show()
