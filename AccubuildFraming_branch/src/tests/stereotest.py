#!/usr/bin/python3

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
from plyfile import PlyData, PlyElement


class StereoGen:
	def depthmap(self, numdisp = 2048,\
			blocksize = 9,\
			calfile = sc.CALIBRATION_FILE_PATH,\
			right = "rightL.png",\
			left = "leftL.png",\
			fromfs = False,\
			plot = True,\
			save = False,\
			out = "depthmap.jpg",\
			pointcloud = False,\
			outpcloud = "pointcloud.pyl"):
		cals = stereo_cal.StereoCalibrate(calfile)
		if (not cals.isCalibrated):
			print("Calibrations are incomplete")
			return
		if (fromfs):
			leftImg = cv2.imread(left,0)
			rightImg = cv2.imread(right,0)
		else:
			src = stereosrc.StereoSource()
			leftImg = src.getLeft()
			rightImg = src.getRight()
		depthMap,_ = pl.getDepthMap(numdisp,blocksize,leftImg,rightImg,cals)
		if(pointcloud):
			cloud = pl.getPointCloud(depthMap,cals)
			PlyData([cloud]).write('test.ply')
		if(plot):
			if(PYPLOT_IMPORT):
				plt.imshow(depthMap)
				plt.show()
			else:
				print('Plot not generated. Could not import pyplot module')
		if(save):
			cv2.imwrite(out,depthMap);

	def recal(self, ldir = sc.LEFT_CAM_CAL_DIR, \
		rdir = sc.RIGHT_CAM_CAL_DIR, \
		calfile = sc.CALIBRATION_FILE_PATH):
		cals = stereo_cal.StereoCalibrate(calfile)
		cals.calibrateFromFs(ldir,rdir,sc.CHESSBOARD_EXT,sc.CHESSBOARD_DIMS)
fire.Fire(StereoGen)
