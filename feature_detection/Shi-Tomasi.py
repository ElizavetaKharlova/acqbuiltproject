import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


#imports the image
img = cv.imread('depthmap.jpg', 0)
#gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
gray = np.float32(img)
#time to do corner detection

corners = cv.goodFeaturesToTrack(gray,25,0.01,10)
corners = np.int0(corners)

print(corners)
for i in corners:
    x,y = i.ravel()
    cv.circle(img, (x,y), 3, 255, -1)

img2 = cv.drawKeypoints(img, corners ,0 ,color = (255,0,0))
#cv.imwrite("ShiTomasi_image.png",corners)
while 1:
    cv.imshow('ShiTomasi_image',img2)
    if cv.waitKey(1) == 0x1b: #ESC
        print('ESC pressed. Exiting ...')
        break
