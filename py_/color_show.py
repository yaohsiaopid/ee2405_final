import cv2
import sys
import matplotlib.pyplot as plt
from calibrate import *
# vc = cv2.VideoCapture(1)
# _, img = vc.read()
img = cv2.imread('a3.jpg')
img = calibrate(img)
if sys.argv[1] == "BGR2HLS":
    print("Config: BGR2HLS")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2HLS)
    # img = cv2.GaussianBlur(img,(5,5),0)
    
elif sys.argv[1] == "BGR2HSV":
    print("Config: BGR2HSV")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # img = cv2.GaussianBlur(img,(5,5),0)

else:
    print("Config: BGR2RGB")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # img = cv2.GaussianBlur(img,(5,5),0)
plt.imshow(img)
plt.show()
