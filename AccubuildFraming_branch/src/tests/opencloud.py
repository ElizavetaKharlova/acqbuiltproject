#!/usr/bin/python3


# For playing with the cloud files.

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

cloud = np.load('pcloud3.npy')
cloud_ind = np.argsort(-cloud[:,2]) # change the axis
cloud_sorted = cloud[cloud_ind]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
c = 'b'
m = 'o'
ax.scatter(cloud[:,0], cloud[:,1], cloud[:,2], c=c, marker=m)
#ax.scatter(cloud_sorted[10000:100000,0], cloud_sorted[10000:100000,1], cloud_sorted[10000:100000,2], c=c, marker=m)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
