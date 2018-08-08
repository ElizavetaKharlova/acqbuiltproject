#import cv2
#import numpy as np
#
#
##img = cv2.imread('right_2_depth_Depth.png')
#img = cv2.imread('right_2_depth_Depth.raw')
#
#print(img)

#cv2.imshow('image',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#import rawpy
#import imageio
#
#path = 'left_side_depth_Depth.raw'
#with rawpy.imread(path) as raw:
#    rgb = raw.postprocess()
#imageio.imsave('default.tiff', rgb)

for line in open('left_side_depth_Depth.raw', 'r').readline():
    print(float(x) for x in line.split())
