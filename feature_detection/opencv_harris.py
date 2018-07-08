import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

#imports the image
img = cv.imread('depthmap.jpg', 0)
#gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
gray = np.float32(img)
#time to do corner detection

dst = cv.cornerHarris(gray, 2, 3, 0.04)

#dst = cv.dilate(dst, None)

#img[dst>0.01*dst.max()]=[0,0,255]

cv.imwrite("Harris_image.png",dst)
while 1:
    cv.imshow('Fast_image',dst)
    if cv.waitKey(1) == 0x1b: #ESC
        print('ESC pressed. Exiting ...')
        break
