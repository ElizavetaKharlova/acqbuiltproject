import cv2 as cv
import numpy as np


img1 = cv.imread('./images/Blender/depthmap1.jpg', 0)
img2 = cv.imread('./images/Blender/warped1_topRight.jpg', 0 )

orb = cv.ORB_create(nfeatures = 1000, scoreType = cv.ORB_FAST_SCORE)
# perform the detection and computation on the first image

#kp1 = orb.detect(img1,None)
#des1 = orb.compute(img1, kp1)

kp1, des1 = orb.detectAndCompute(img1, None)
#Perform the feature detection and computatipn on the second images
kp2, des2 = orb.detectAndCompute(img2, None)

# now invoke the brute force matcher


bf = cv.BFMatcher_create(cv.NORM_HAMMING, crossCheck = True)

matches = bf.match(des1, des2)

#ort them in order of distance:
matches = sorted(matches, key = lambda x:x.distance)

#draw only the first 10 matches

img3 = cv.drawMatches(img1, kp1, img2, kp2, matches[100:] ,None ,flags=2)
im3s = cv.resize(img3, (960,540))

cv.imwrite("BFmatch_DM1toW3_knn.png",img3)

while 1:
	cv.imshow('ORB', im3s)
	if cv.waitKey(1) == 0x1b:
		print('ESC pressed. Exiting ...')
		break
