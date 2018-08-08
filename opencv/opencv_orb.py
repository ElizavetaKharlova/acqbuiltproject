import cv2 as cv
import numpy as np
#from matplotlib import pyplot as plt

#img = cv.imread('./images/tx2_camera/Left.png', 0)
img = cv.imread('depth_new.jpg', 0)
#Orb initialization
orb = cv.ORB_create(nfeatures=10000, scoreType = cv.ORB_FAST_SCORE)
#keypoints
kp = orb.detect(img,None)

kp, des = orb.compute(img, kp)

img2 =cv.drawKeypoints(img, kp, 0,color=(0,255,0), flags = 0)


cv.imwrite("Orb_depthmap_warped1.png",img2)
while 1:
	cv.imshow('ORB', img2)
	if cv.waitKey(1) == 0x1b:
		print('ESC pressed. Exiting ...')
		break
