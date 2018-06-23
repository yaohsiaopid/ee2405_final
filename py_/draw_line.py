import sys
import time
import cv2
import numpy as np
from calibrate import *
#from cv2.dnn import readNetFromTensorflow
#from cv2.dnn import blobFromImage
from sklearn.cluster import KMeans, DBSCAN
import serial
import matplotlib.pyplot as plt

def rtheta2ab( r, theta ):
	rho_avg = r
	theta_avg = theta
	a = np.cos(theta_avg)
	b = np.sin(theta_avg)
	x0 = a*rho_avg
	y0 = b*rho_avg
	A = -a/b
	B = (a/b*x0+y0)
	return A,B

def draw_line_rth( img, r, theta ):
	rho_avg = r
	theta_avg = theta
	a = np.cos(theta_avg)
	b = np.sin(theta_avg)
	x0 = a*rho_avg
	y0 = b*rho_avg
	x1 = int(x0 + 1000*(-b))
	y1 = int(y0 + 1000*(a))
	x2 = int(x0 - 1000*(-b))
	y2 = int(y0 - 1000*(a))
	cv2.line(img,(x1,y1),(x2,y2),(0,255,255),8)

def edge_cluster( lines, fileindex, db_eps=30, db_min_samples=5, dump=False, filename="", img=None ):
	db = DBSCAN( eps=db_eps, min_samples=db_min_samples ).fit(lines)
	num_of_lines = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)

	ret_list = []
	if not img is None: img_lined = img.copy()

	for i in range(0,num_of_lines):
		indices = np.where(db.labels_==i)
		rho_avg, theta_avg = np.median(lines[indices], axis=0)
		A, B = rtheta2ab( rho_avg, theta_avg )
		try:
			draw_line_rth( img_lined, rho_avg, theta_avg )
		except: pass
		print("Line #", str(i), ": A = ", A, ", B = ", B)
		ret_list.append((A,B))

	if dump:
		cv2.imwrite( filename, img_lined )
	return ret_list

def get_range( img, low, high, base, erode_kernel_size=(5,5), erode_iteration=2, dilate_kernel_size=(5,5), dilate_iteration=2, canny_low=80, canny_high=120, hough_rho=1, hough_theta=np.pi/180, hough_threshold=25, dump=False, filename="" ):

	cvt = cv2.cvtColor(img, base)

	if not base == cv2.COLOR_RGB2GRAY:
		cvt_th = cv2.inRange(cvt, low, high)
		### The cv2.inRange  function expects three arguments: the first is the image  were we are going to perform color detection, the second is the lower  limit of the color you want to detect, and the third argument is the upper  limit of the color you want to detect.
		### After calling cv2.inRange, a binary mask is returned, where white pixels (255) represent pixels that fall into the upper and lower limit range and black pixels (0) do not.
		fileindex = str(int(low[0]))
	else:
		cvt = cv2.GaussianBlur(cvt,(5,5),0)
		# plt.imshow(cvt)
		# plt.show()
		_, cvt_th = cv2.threshold( cvt, low, high, cv2.THRESH_BINARY )
		fileindex = str(low)
	
	# cvt_th = cv2.erode(	cvt_th, np.ones( erode_kernel_size, np.uint8), iterations=erode_iteration )
	cvt_th = cv2.dilate(cvt_th, np.ones( dilate_kernel_size, np.uint8), iterations=dilate_iteration )
	cvt_th = cv2.erode(	cvt_th, np.ones( erode_kernel_size, np.uint8), iterations=erode_iteration )
	if dump:
		filename_index = filename.find('/')+1
		fi = filename_index
		cv2.imwrite( filename[:fi] + "th_" + filename[fi:], cvt_th )

	edges = cv2.Canny( cvt_th, canny_low, canny_high )
	if dump:
		filename_index = filename.find('/')+1
		fi = filename_index
		cv2.imwrite( filename[:4] + "canny_" + filename[4:], edges )

	lines_hough = cv2.HoughLines( edges,hough_rho, hough_theta, hough_threshold )
	if np.shape(lines_hough) == ():
		print("No line detected")
		return []
	print("j")
	lines = lines_hough.swapaxes(0,1)[0]
	ret_list = edge_cluster( lines, fileindex, dump=dump, filename=filename , img=img)
	# plt.imshow(img)
	# plt.show()
	return ret_list
	
def get_yellow( img, dump=False, filename="" ):
	return get_range( img, np.array([25, 110, 190], np.uint8), np.array([35, 145, 235], np.uint8), cv2.COLOR_BGR2HSV, dump=dump, filename=filename )

def get_white( img, dump=False, filename="" ):
	return get_range( img, np.array([75, 0, 200], np.uint8), np.array([110,30,255], np.uint8), cv2.COLOR_BGR2HSV, dump=dump, filename=filename)
def get_red(img, dump=False, filename=""):
	# return get_range( img, np.array([165,100,200], np.uint8), np.array([178,170,220], np.uint8), cv2.COLOR_BGR2HSV, dump=dump, filename=filename )
	return get_range( img, np.array([170,85,75], np.uint8), np.array([200, 110, 120], np.uint8), cv2.COLOR_BGR2RGB, dump=dump, filename=filename )
def get_gray( img, dump=False, filename=""):
	line_gry = get_range(img, 180,255, cv2.COLOR_RGB2GRAY, dump=dump, filename=filename)
if __name__ == "__main__":
	global filename, f, start_time
	# filename = "test"
	# vc = cv2.VideoCapture(1)
	# _, img = vc.read()
	img = cv2.imread('{}.jpg'.format(sys.argv[1]))
        #time.sleep(0.5)
	img = calibrate(img)
	# cv2.imwrite('result/a.jpg', img)
	# line_yellows = get_yellow( img, dump=True, filename="result/0.jpg" )
	# lin = get_white(img, dump=True, filename="result/1.jpg")
	line_reds    = get_red(img, dump=True, filename="result/2.jpg" )
