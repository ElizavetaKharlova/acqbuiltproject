import cv2

RIGHT_CAM = 'Right'
LEFT_CAM  = 'Left'

LEFT_CAM_CAL_DIR = './calibration/' + LEFT_CAM + '/'
RIGHT_CAM_CAL_DIR = './calibration/' + RIGHT_CAM + '/'

CHESSBOARD_DIMS = (7, 6)
CHESSBOARD_EXT = '.png'

CORNERS_TERM = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)

CALIBRATION_FILE_PATH = 'calibrate.xml'

LEFT_RMS_ERROR = 'lRms'
LEFT_K_MATRIX  = 'lKmat'
LEFT_D_MATRIX  = 'lDmat'

RIGHT_RMS_ERROR  = 'rRms'
RIGHT_K_MATRIX   = 'rKmat'
RIGHT_D_MATRIX   = 'rDmat'

STEREO_RMS_ERROR = 'sRms'

STEREO_LEFT_MAP_1 = 'slMap1'
STEREO_LEFT_MAP_2 = 'slMap2'

STEREO_RIGHT_MAP_1 = 'srMap1'
STEREO_RIGHT_MAP_2 = 'srMap2'

STEREO_Q_MATRIX = 'sQMat'

IMG_CROP_OFFSET = 200
