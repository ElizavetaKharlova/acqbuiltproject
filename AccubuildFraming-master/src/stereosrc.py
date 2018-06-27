import os, tempfile
import subprocess
import cv2
import pexpect

LEFT  = 'left'
RIGHT = 'right'

NVGSTCAPTURE_ARGS  = '--exposure-time=1 \
					  --contrast=1 \
					  --image-res=10 \
					  --tnr-mode=2 \
					  --tnr-strength=1.0 '
NVGSTCAPTURE_LEFT  = '--sensor-id=0 --file-name='
NVGSTCAPTURE_RIGHT = '--sensor-id=2 --file-name='

class StereoSource:
	def __init__(self):
		self.left_tmpdir = tempfile.mkdtemp()
		self.right_tmpdir = tempfile.mkdtemp()
		print(self.right_tmpdir)
		print(self.left_tmpdir)
	def getLeft(self):
		nvgst_child = pexpect.spawn('nvgstcapture-1.0 ' + NVGSTCAPTURE_ARGS + NVGSTCAPTURE_LEFT + self.left_tmpdir + '/' + LEFT)
		nvgst_child.expect('.*===== MSENC =====*')
		nvgst_child.sendline('j')
		nvgst_child.expect('.*Image Captured.*')
		nvgst_child.terminate()
		img = self.left_tmpdir + '/' + os.listdir(self.left_tmpdir)[0]
		cvImg = cv2.imread(img,0)
		os.remove(img)
		return cvImg

	def getRight(self):
		nvgst_child = pexpect.spawn('nvgstcapture-1.0 ' + NVGSTCAPTURE_ARGS + NVGSTCAPTURE_RIGHT + self.right_tmpdir + '/' + RIGHT)
		nvgst_child.expect('.*===== MSENC =====.*')
		nvgst_child.sendline('j')
		nvgst_child.expect('.*Image Captured.*')
		nvgst_child.terminate()
		img = self.right_tmpdir + '/' + os.listdir(self.right_tmpdir)
		cvImg = cv2.imread(img,0)
		os.remove(img)
		return cvImg
