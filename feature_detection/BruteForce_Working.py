#!/usr/bin/env python
#this is the working version of the brute force matcher


import cv2 as cv
import np as

img1 = cv.imread('path/to/image1', 0)
img2 = cv.imread('Path/to/image2', 0)

orb = cv.ORB_create()

kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

#matcher
bf = cv.BFMatcher_create(cv.NORM_HAMMING, crossCheck= True)

matches = bf.Match(des1, des2)

# this sorts the matches by the similarity between the keypoints
'''
ASIDE: I think that the sorting may actually sort lowest to highest, which
may be why we saw very bad matching.

'''

# TODO: Look into the later part of the matches.distance values
matches = sorted(matches, key = lambda x:x.distance)

img3 = cv.drawMatches(img1, kp1, img2, kp2, matches[100], None, flags = 2)
# resize the image for easier examination
img3s = cv.resize(img3, (960, 540))

# save the image:
cv.imwrite("File_name ", img3)

# display the image
while 1:
    cv.imshow('MATCHING', img3s)
    if cv.waitkey(1) == 0x1b:
        print('ESC pressed. Closing image ...')
        break
