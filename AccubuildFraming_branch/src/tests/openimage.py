
# For warping the depthmap images.


import numpy as np
import cv2
import sys
try:
    from matplotlib import pyplot as plt
    PYPLOT_IMPORT = True
except:
    PYPLOT_IMPORT = False
sys.path.append('../')
import const as sc
import calibrate as stereo_cal
import stereopipeline_nopcl as pl
import stereosrc
import fire
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import argparse
from skimage import data

image = cv2.imread('depthmap3.jpg')
print(image[700:800,700])
image = cv2.resize(image, (914, 760), cv2.INTER_NEAREST)

def define_rect(image):
    """
        Define a rectangular window by click and drag your mouse.
        
        Parameters
        ----------
        image: Input image.
        """
    
    clone = image.copy()
    rect_pts = [] # Starting and ending points
    win_name = "image" # Window name
    re = []
    
    def select_points(event, x, y, flags, param):
        
        nonlocal rect_pts
        if event == cv2.EVENT_LBUTTONDOWN:
            rect_pts = [(x, y)]
    
        if event == cv2.EVENT_LBUTTONUP:
            rect_pts.append((x, y))
            re.append((x,y))
            
            # draw a rectangle around the region of interest
            cv2.rectangle(clone, rect_pts[0], rect_pts[1], (0, 255, 0), 2)
            cv2.imshow(win_name, clone)

    cv2.namedWindow(win_name)
    cv2.setMouseCallback(win_name, select_points)

    while True:
    # display the image and wait for a keypress
        cv2.imshow(win_name, clone)
        key = cv2.waitKey(0) & 0xFF
    
        if key == ord("r"): # Hit 'r' to replot the image
            clone = image.copy()
        
        elif key == ord("c"): # Hit 'c' to confirm the selection
            break

    # close the open windows
    cv2.destroyWindow(win_name)

    return rect_pts, re



# Points of the target window
points, re = define_rect(image)

# now that we have our rectangle of points, let's compute
# the width of our new image
(tl, tr, br, bl) = re
widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

# ...and now for the height of our new image
heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

# take the maximum of the width and height values to reach
# our final dimensions
maxWidth = max(int(widthA), int(widthB))
maxHeight = max(int(heightA), int(heightB))

# construct our destination points which will be used to
# map the screen to a top-down, "birds eye" view
dst = np.array([
    [0, 0],
    [maxWidth - 1, 0],
    [maxWidth - 1, maxHeight - 1],
    [0, maxHeight - 1]], dtype = "float32")

# calculate the perspective transform matrix and warp
# the perspective to grab the screen
rec = np.array(re)
rect = rec.astype(np.float32)

M = cv2.getPerspectiveTransform(rect, dst)
orig = image
warp = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))
print(warp.shape)
cv2.imwrite('warped_jj.jpg',warp)
cv2.imshow('o', warp)
cv2.waitKey(0)
