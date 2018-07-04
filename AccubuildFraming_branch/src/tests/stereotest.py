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


'''
	The object that is called as a CLI using fire

	Invoking from the command line like so:
	python stereotest.py _func_ _param_-_param_

'''

class StereoGen:
	'''
		@function depthmap(self,numdisp, blocksize, calfile, right, left, fromfs, plot, \
		save, out, pointcloud, outpcloud)

		@param numdisp
		The number of disparities for the depth map. OpenCV parameter.

		@param blockSize
		The size of the block to do correlation with.

		@parm calfile
		Calibration values for the cameras that took the left and right images.

		@param right
		Right camera frame in .png image format.

		@param left
		Left camera frame in .png image format.

		@param fromfs
		Boolean that determines if the function will load images from opencv or
		from the src directory.

		@param plot
		Boolean that determines if the depthmap will be shown as a plot

		@param save
		Boolean that determines if the depthmap will be saved.

		@param out
		File that the depthmap is saved to.
		@param pointcloud
		This boolean allows you to generate a pointcloud out of the depthMap
		and write it to test.ply

		@outcloud
		Doesn't look like anything to me

		@return
		Prints errors if certain critera are not met and writes a depthmap to
		the out parameter

	'''
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

'''
	@function recal (self,ldir, rdir, calfile)
	recalibrates the stereo_cal method using the provided directories.

	@param ldir
	This is the directory that contains all the left camera calibration
	images. Calibration is done with the chessboard calibration method.

	@param rdir
	This is the directory that contains all the right camera calibration
	images. Calibration is done with the chessboard calibration method.

	@param calfile
	This is the calibration file that is passed into the stereo_cal method.
'''
	def recal(self, ldir = sc.LEFT_CAM_CAL_DIR, \
		rdir = sc.RIGHT_CAM_CAL_DIR, \
		calfile = sc.CALIBRATION_FILE_PATH):
		cals = stereo_cal.StereoCalibrate(calfile)
		cals.calibrateFromFs(ldir,rdir,sc.CHESSBOARD_EXT,sc.CHESSBOARD_DIMS)

#### main code #####
'''
Launches the StereoGen class as a CLI command using Fire
'''
fire.Fire(StereoGen)
