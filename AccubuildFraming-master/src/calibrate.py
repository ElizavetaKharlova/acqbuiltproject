'''
    This file describes the StereoCalibrate object and it's 
    methods. The StereoCalibrate object is used for loading, saving
    and working with camera calibration values and maps. It saves 
    the calibration file to "calibration.xml". The "calibration.xml"
    file can be generated from a set of calibration images from both the 
    left and the right camera imaging a checkerboard. Check 
    https://docs.opencv.org/3.4.1/dc/dbb/tutorial_py_calibration.html
    for camera calibration
'''

import cv2
import numpy as np
import os
import const as sc

'''
    The object representing calibrations, with methods to calibrate
'''
class StereoCalibrate:
    '''
        @function __init__(self,calibration)
        Constructor for the StereoCalibration object

        @param calibrationFpDir
        String directory of the calibration.xml file where calibration
        paramaters will be loaded from (if it exists) or where
        the parameters will be stored (if they dont exist)
    '''
    def __init__(self,calibrationFpDir):
        self.isCalibrated = True
        self.calibrationFpDir = calibrationFpDir
        fs = cv2.FileStorage(self.calibrationFpDir,cv2.FILE_STORAGE_READ)
        if(not fs.isOpened):
            self.isCalibrated = False
            print("Could not find file calibrations")
        else:
            try:
                self.lRms = fs.getNode(sc.LEFT_RMS_ERROR)
                self.lCameraMatrix = fs.getNode(sc.LEFT_K_MATRIX).mat()
                self.lDistCoeffs = fs.getNode(sc.LEFT_D_MATRIX).mat()
                self.rRms = fs.getNode(sc.RIGHT_RMS_ERROR)
                self.rCameraMatrix = fs.getNode(sc.RIGHT_K_MATRIX).mat()
                self.rDistCoeffs = fs.getNode(sc.RIGHT_D_MATRIX).mat()
                self.slMap1 = fs.getNode(sc.STEREO_LEFT_MAP_1).mat()
                self.slMap2 = fs.getNode(sc.STEREO_LEFT_MAP_2).mat()
                self.srMap1 = fs.getNode(sc.STEREO_RIGHT_MAP_1).mat()
                self.srMap2 = fs.getNode(sc.STEREO_RIGHT_MAP_2).mat()
                self.qMatrix = fs.getNode(sc.STEREO_Q_MATRIX).mat()
                self.isCalibrated = (self.lRms is not None and \
                              self.lCameraMatrix is not None and \
                              self.lDistCoeffs is not None and \
                              self.rRms is not None and \
                              self.rCameraMatrix is not None and \
                              self.rDistCoeffs is not None and \
                              self.slMap1 is not None and \
                              self.slMap2 is not None and \
                              self.srMap1 is not None and \
                              self.srMap2 is not None and \
                              self.qMatrix is not None)
                fs.release()
            except:
                self.isCalibrated = False
                print("Could not find all paramaters in calibration file")

    '''
        @function _getImgList(self,directory,ext)
        Get the list of all the files in a directory

        @param directory
        String path to the directory that contains the images

        @param ext
        The file extension of the images (png, jpeg, etc)

        @return
        String of all the image paths of a particular extension
        in an image
    '''

    def _getImgList(self,directory,ext):
        dirList = []
        imgList = []
        for entry in os.listdir(directory):
            if (os.path.isfile(directory + entry)) and entry[-4:-1] + (entry[-1]) == ext:
                dirList.append(directory+entry)
        dirList.sort()
        for dirs in dirList:
            imgList.append(cv2.imread(dirs, cv2.IMREAD_GRAYSCALE))    
        return imgList

    '''
        @function _getCorners(self,imgs,dims)
        Returns a list of all the corners in a set of images
        
        @param imgs
        List of images to get corners from, in the form of
        opencv numpy arrays

        @param dims
        Dimension of the checkerboard in the form of an array
    '''

    def _getCorners(self,imgs,dims):
        cornersList = []
        for img in imgs:
            retval,corners = cv2.findChessboardCorners(img,dims)
            if retval:
                subPixCorners = cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), sc.CORNERS_TERM)
            cornersList.append(subPixCorners)
        return cornersList

    '''
        @function _getObjPoints(self,dims)
        bottom text

        @param dims
        Dimension of the checkerboard

        @return
        An array that opencv needs for some reason for calibration
    '''

    def _getObjPoints(self,dims):
        patternPoints = np.zeros((np.prod(dims), 3), np.float32)
        patternPoints[:, :2] = np.indices(dims).T.reshape(-1, 2)
        return patternPoints

    '''
        @function _getCameraMatrix(self,imgPoints,objPoints,dims)
        Get the camera calibration matrix

        @param imgPoints
        List of the checkerboard corners

        @param objPoints
        Dumb arbitrary matrix that opencv functions need

        @param dims
        Dimensions of the checkerboard as an array

        @return
        The distortion calibration matrix
    '''

    def _getCameraMatrix(self,imgPoints,objPoints,dims):
        objPointsList = []
        for img in imgPoints:
            objPointsList.append(objPoints)
        return cv2.calibrateCamera(objPointsList, imgPoints, dims, None,None)

    '''
        @function _getStereoMatrix(self,objPoints,lCorners,rCorners,
        lCameraMatrix,lDistCoeff,rCameraMatrix,rDistCoeffs,dims)
        Get the stereoscopic calibration matrix

        @param objPoints
        Array of points that opencv needs

        @param lCorners
        Array of corner coordinates from the left image

        @param rCorners
        Array of corner coordinates from the right image

        @param lCameraMatrix
        The camera distortion matrix for the left camera

        @param lDistortionMatrix
        The camera distortion coefficients for the left camera

        @param rCameraMatrix
        The camera distortion matrix for the right camera

        @param rDistortionMatrix
        The camera distortion coefficients for the right camera

        @param dims
        The dimensions of the checkerboard

        @return
        The stereo calibration matrix for the two cameras
    '''

    def _getStereoMatrix(self,objPoints, lCorners, rCorners, lCameraMatrix, lDistCoeffs ,rCameraMatrix, rDistCoeffs, dims):
        objPointsList = []
        for corners in lCorners:
            objPointsList.append(objPoints)
        return cv2.stereoCalibrate(objPointsList, lCorners, rCorners, lCameraMatrix, lDistCoeffs, rCameraMatrix, rDistCoeffs, dims)

    '''
        @function _writeStereoMatrix
        Function that writes the calibrations to the filesystem

        @return
        True if the calibrations have been written, false otherwise
    '''

    def _writeStereoMatrix(self):
        fs = cv2.FileStorage(self.calibrationFpDir,cv2.FILE_STORAGE_WRITE)
        if(not fs.isOpened):
            print("File not open")
            return False
        fs.write(sc.LEFT_RMS_ERROR,self.lRms)
        fs.write(sc.LEFT_K_MATRIX,self.lCameraMatrix)
        fs.write(sc.LEFT_D_MATRIX,self.lDistCoeffs)
        fs.write(sc.RIGHT_RMS_ERROR,self.rRms)
        fs.write(sc.RIGHT_K_MATRIX,self.rCameraMatrix)
        fs.write(sc.RIGHT_D_MATRIX,self.rDistCoeffs)
        fs.write(sc.STEREO_RMS_ERROR,self.sRms)
        fs.write(sc.STEREO_LEFT_MAP_1,self.slMap1)
        fs.write(sc.STEREO_LEFT_MAP_2,self.slMap2)
        fs.write(sc.STEREO_RIGHT_MAP_1,self.srMap1)
        fs.write(sc.STEREO_RIGHT_MAP_2,self.srMap2)
        fs.write(sc.STEREO_Q_MATRIX,self.qMatrix)
        fs.release()
        print("Calibrations written to file")
        return True

    '''
        @function calibrate(self,lImgs,rImgs,chessBoardDims)
        Generate calibration for the object

        @param lImgs
        List of the images from the left cameras as numpy arrays

        @param rImgs
        List of the images from the right cameras as numpy arrays
    '''

    def calibrate(self,lImgs,rImgs,chessBoardDims):
        dims = lImgs[0].shape[:2]

        objPoints = self._getObjPoints(chessBoardDims)
        lCorners = self._getCorners(lImgs,chessBoardDims)

        rCorners = self._getCorners(rImgs,chessBoardDims)

        self.lRms, self.lCameraMatrix, self.lDistCoeffs, *_ = self._getCameraMatrix(lCorners, objPoints, dims)

        self.rRms, self.rCameraMatrix, self.rDistCoeffs, *_ = self._getCameraMatrix(rCorners, objPoints,dims)

        self.sRms, _, _, _, _, R, T, *_ = self._getStereoMatrix(objPoints, lCorners, rCorners, self.lCameraMatrix, self.lDistCoeffs, self.rCameraMatrix, self.rDistCoeffs, dims)

        lR,rR,lP,rP,self.qMatrix,*_ = cv2.stereoRectify(self.lCameraMatrix,self.lDistCoeffs,self.rCameraMatrix,self.rDistCoeffs,dims,R,T)

        self.slMap1,self.slMap2 = cv2.initUndistortRectifyMap(self.lCameraMatrix,self.lDistCoeffs,lR,lP,(dims[1],dims[0]),cv2.CV_16SC2)

        self.srMap1,self.srMap2 = cv2.initUndistortRectifyMap(self.rCameraMatrix,self.rDistCoeffs,rR,rP,(dims[1],dims[0]),cv2.CV_16SC2)

        self._writeStereoMatrix()

    '''
        @function calibrateFromFs(self,lImgDir,rImgDir,imgExt,chessBoardDims)
        Generate calibration parameters from the filesystem

        @param lImgDir
        The directory containing the images from the left camera. Images
        should be named "Left1","Left2","Left3" etc

        @param rImgDir
        The directory containing the images from the right camera. Images
        should be named "Right1","Right2","Right3" etc

        @param imgExt
        The extension of the images in the directory

        @param chessBoardDims
        The dimensions of the chessboard
    '''

    def calibrateFromFs(self,lImgDir, rImgDir, imgExt, chessBoardDims):
        lImgs = self._getImgList(lImgDir, imgExt)

        print('Loading left camera images ..')

        rImgs = self._getImgList(rImgDir, imgExt)

        print('Loading right camera images ..')

        self.calibrate(lImgs,rImgs,chessBoardDims)

        print('Calibration complete')
