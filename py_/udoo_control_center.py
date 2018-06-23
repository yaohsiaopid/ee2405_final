import sys
import time
import cv2
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
import serial
from calibrate import *
from draw_line import get_yellow, get_range, get_white, get_red
from get_contours import get_gray_countour, contour_dump
from select_contours import contour_leftest, remove_contour, contour_largest
import paho.mqtt.client as mqtt
from scipy.misc import imresize

loc_x = -1
loc_y = -1
label = {0: 'neg', 1: 'pos'}
complete = 0
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("ee2405/id2")


def on_message(client, userdata, msg):
	global loc_x, loc_y
	# parse msg to two x, y
	str = msg.payload.decode("utf-8")
	arr = str.split(",")
	loc_x = int(arr[0])
	loc_y = int(arr[1])
	if msg.payload == b"quit":
		client.disconnect()	

def _control_center( center_point ):
	ang = np.arctan2( center_point[0], center_point[1] )
	print("ang = ", ang)
	turn = 1-abs(ang)
	if turn < 0.1: turn = 0.1
	if ang < 0: turn = -turn
	speed = int(25*abs(turn)+30)
	return speed, turn

def get_contour_center( contour ):
	moment_contour = cv2.moments(contour)
	if moment_contour['m00']:
		moment_contour_x = int(moment_contour['m10']/moment_contour['m00'])
		moment_contour_y = int(moment_contour['m01']/moment_contour['m00'])
		return (moment_contour_x, moment_contour_y)

def get_contour_from_image( img ):
	line_yellows = get_yellow( img )
	line_whites = get_white( img )
	line_reds = get_red( img )
	img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # convert the color image to gray image
	contours = get_gray_countour(img_gray)
	contour_dump( "img/contours_full" + str(int(time.time()*10)) + ".jpg", contours, img)
	_, contours = remove_contour( line_yellows, contours, 1 )
	if len(contours) == 0: return None
	# _, contours = remove_contour( line_whites, contours, -1 )
	# if len(contours) == 0: return None
	contour_left = contour_largest(contours)
	contour_dump( "img/contours_extracted" + str(int(time.time()*10)) + ".jpg", contour_left, img)
	return contour_left, len(line_reds)

def control( contour, s , img):
	contour_center = get_contour_center(contour)
	if contour_center is None: return
	print("contour center = ", contour_center)
	control_vec = np.subtract( (np.shape(img)[1]/2, np.shape(img)[0]), contour_center )
	speed, turn = _control_center( control_vec )
	cmd = "/ServoTurn/run " + str(speed) + " " + "{0:.2f}".format(turn) + " \n"
	print("cmd = ", cmd)
	s.write(cmd.encode())
	print("speed, turn = ", speed, turn)

def nav_to_red():
	for i in range(0,20): vc.read()
	cnt = 0
	while 1:
		start_time = time.time()
		_, img = vc.read()
		img = calibrate(img)

		contour, red_line = get_contour_from_image(img)
		if red_line > 0: 
			cnt += 1 
		else: 
			cnt = 0  
		if cnt >= 5: 
			print(red_line)
			print("jjjdk")
			cmd = "/StopCar/run \n"
			s.write(cmd.encode())
			time.sleep(1)
			break 

		## if not red line or control center notify it already is at red line
		if not contour is None: control(contour,s, img)
		
def scoop_ops(r):
	cmd = "/ScoopOp/run " + str(r) + " \n"
	s.write(cmd.encode())
	ack = s.read(1)

def nav_to_trans():
	# pass the box
	x0 = 3
	y0 = 4
	global loc_x, loc_y
	for i in range(0,20): vc.read()
	while 1:
		start_time = time.time()
		_, img = vc.read()
		img = calibrate(img)

		contour, _ = get_contour_from_image(img)
		######## ???? 
		if ((loc_x - x0)**2+(loc_y - y0)**2)**0.5 < 3:
			cmd = "/StopCar/run \n"
			s.write(cmd.encode())
			time.sleep(1)
			break
		if not contour is None: control(contour,s, img)
		
def keras_scoop():
	for i in range(0,20): vc.read()
	net = cv2.dnn.readNetFromTensorflow("./src/arm_mobil_e30.pb")
	dic = { 0: 0, 1:0}
	for _ in range(10):
		ret, frame = vc.read()
		frame_resize = imresize(frame, (128, 128))
		frame = cv2.dnn.blobFromImage(frame)
		net.setInput(frame)
		pred = net.forward()
		ans = pred[0, :, 0, 0].argmax(axis=-1)
		dic[ans] = dic[ans] + 1

	if dic[1] > dic[0]:
		print("see pokemon!!!") #dic[1] see pokemon
		return 0  # dic[1] see pokemon
	else:
		return 1

def update_bar():
	global complete
	complete += 20
	mesg = "2_" + str(complete)
	publish.single("ee2405/complete", mesg, hostname="host_ip")
	if complete > 100:
		complete = 0
	

if __name__ == "__main__":
	s = serial.Serial("/dev/ttyACM0")
	# s = serial.Serial("/dev/tty.usbmodem1412")
	vc = cv2.VideoCapture(1)
	for i in range(0,20): vc.read()
	

	### mqtt
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("192.168.1.41", 1883, 60)  # host ip
	# listening in the background thread
	client.loop_start()


	### 
	nav_to_red()  # 20
	update_bar()
	time.sleep(1)
	# #### keras 
	num = keras_scoop() # 40
	update_bar()
	time.sleep(0.5)
	scoop_ops(num) # 80
	update_bar()
	time.sleep(1)
	nav_to_trans() # 100
	update_bar()
	time.sleep(1)
	cmd = "/UTurn/run \n"
	s.write(cmd.encode())
	update_bar()
	
	
