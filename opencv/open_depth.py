import cv2
import numpy as np


def preprocess(img):

    #img = cv2.resize(img, (960,540), cv2.INTER_NEAREST)
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    dilation = cv2.dilate(opening,kernel,iterations = 1)

#    cv2.imwrite('depth_new.jpg', dilation)

#    cv2.imshow('image',dilation)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()

    return dilation

