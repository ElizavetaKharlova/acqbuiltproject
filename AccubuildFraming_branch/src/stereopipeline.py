import numpy as np
import cv2
import const as sc
import math
import calibrate as stereo_cal
from plyfile import PlyData, PlyElement
#import pcl

'''
    @function getDepthMap(numDisp,bSize,lImg,rImg,cals)
    Get the depth map in reference to the left image

    @param numDisp
    The number of disparities for the depth map. OpenCV parameter

    @param bSize
    The size of the block to do correlation with

    @param lImg
    The image from the left camera

    @param rImg
    The image from the right camera

    @param cals
    The StereoCalibration object containing the calibration parameters
'''

def getDepthMap(numDisp,bSize,lImg,rImg,cals):
    imgLUndistort = cv2.undistort(lImg,cals.lCameraMatrix,cals.lDistCoeffs)
    imgRUndistort = cv2.undistort(rImg,cals.rCameraMatrix,cals.rDistCoeffs)

    imgLRemap = cv2.remap(imgLUndistort,cals.slMap1,cals.slMap2,cv2.INTER_LINEAR)
    imgRRemap = cv2.remap(imgRUndistort,cals.srMap1,cals.srMap2,cv2.INTER_LINEAR)

    imgLLarge = np.zeros((imgLRemap.shape[0],imgLRemap.shape[1]+numDisp),dtype = np.uint8)
    imgRLarge = np.zeros((imgRRemap.shape[0],imgRRemap.shape[1]+numDisp),dtype = np.uint8)

    imgLLarge[:,numDisp:(numDisp + imgLRemap.shape[1])] = imgLRemap;
    imgRLarge[:,numDisp:(numDisp + imgRRemap.shape[1])] = imgRRemap;

    stereo = cv2.StereoBM.create(numDisparities = numDisp, blockSize = bSize)
    
    disparityCropped = stereo.compute(imgLLarge,imgRLarge)[:,numDisp+sc.IMG_CROP_OFFSET:numDisp + lImg.shape[1]]        
    
    return disparityCropped,imgLRemap

'''
    @function getPointCloud(dispMap,cals)
    Get the point cloud from a disparity map

    @param dispMap
    The disparity map or the depth map

    @param cals
    The calibration object containing the calibration constant

    @return
    Point cloud as an array of 3 touples
'''

def getPointCloud(dispMap,cals):
    p = pcl.PointCloud() 
    validPoints = cv2.reprojectImageTo3D(dispMap,cals.qMatrix)[np.where(dispMap != -16)].squeeze()
    p.from_list(validPoints)
    fil = p.make_statistical_outlier_filter()
    fil.set_mean_k(100)
    fil.set_std_dev_mul_thresh (0.01)
    filtPoints = np.array(fil.filter().to_list())
    cloud = np.empty(len(filtPoints),dtype=[('x', 'f4'), ('y', 'f4'),('z', 'f4')])
    cloud['x'] = filtPoints[:,0]
    cloud['y'] = filtPoints[:,1]
    cloud['z'] = filtPoints[:,2]
    cloud_element = PlyElement.describe(cloud,'vertex')
    return cloud_element
