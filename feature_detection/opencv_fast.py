import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


#imports the image
img = cv.imread('depthmap.jpg', 0)
#gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
#gray = np.float32(gray)
#time to do corner detection

fast = cv.FastFeatureDetector_create()

kp = fast.detect(img,None)

img2 = cv.drawKeypoints(img, kp,0 ,color = (255,0,0))

cv.imwrite("Fast_image.png",img2)
while 1:
    cv.imshow('Fast_image',img2)
    if cv.waitKey(1) == 0x1b: #ESC
        print('ESC pressed. Exiting ...')
        break
