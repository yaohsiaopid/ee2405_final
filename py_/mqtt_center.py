import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import sys
import time
import cv2
import numpy as np
import time
from selenium import webdriver
host_id = "192.168.1.66"
bean = sys.argv[1]
get_msg = 0
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ee2405/complete")


def on_message(client, userdata, msg):
    global get_msg
    print(msg.topic+" "+str(msg.payload))
    # "<id>_........."
    get_msg = 1
    if msg.payload == b"quit":
        client.disconnect()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host_id, 1883, 60) # host ip
# listening in the background thread
client.loop_start()

## 720(h) x 1280(w)
# initialing publisher

def getCoord(img, base, min, max):
    cvt = cv2.cvtColor(img, base)
    cvt_th = cv2.inRange(cvt, min, max)
    arr = np.array(cvt_th)
    stats = np.where(arr > 0)
    cnt = len(stats[0])
    if cnt < 10:
        return -1, -1
    coord = np.sum(stats, axis=1)*1.0/cnt
    return int(coord[1]), int(coord[0]) # x, y with origin (0,0) at left upper point of the window
cnt = 1
#browser = webdriver.Firefox()
#browser.get('file:///Users/yaohsiao/Documents/GDUni/Courses/2018%20Spring/Embedded%20System/final_py/a.html')
while(1):
    vc = cv2.VideoCapture(0)
    _, img = vc.read()
    
    #### Blue
    # img = cv2.imread('frame.jpg')

    # x1, y1 = getCoord(img, cv2.COLOR_BGR2HLS, np.array([100, 85, 200], np.uint8), np.array([110, 100, 240], np.uint8))
    x1 = 60
    y1 = 310    
    msg = str(x1) + "," + str(y1) + "," + str(bean)
    publish.single("ee2405/id1", msg, hostname=host_id)
    ii = cv2.circle(img, (x1, y1, ), 20, (0, 0, 255), -1)
    time.sleep(.01)
    ### Red
    x2, y2 = getCoord(img, cv2.COLOR_BGR2RGB, np.array([165, 45, 40], np.uint8), np.array([185, 55, 60], np.uint8))
    
    if get_msg == 1:
        x2 = 3
        y2 = 4
    msg = str(x2) + "," + str(y2)
    publish.single("ee2405/id2", msg, hostname=host_id)
    time.sleep(.01)
    ii = cv2.circle(ii, (x2, y2), 20, (0, 0, 255), -1)
    ### Green
    x3, y3 = getCoord(img, cv2.COLOR_BGR2HLS, np.array([65, 85, 95], np.uint8), np.array([75, 95, 120], np.uint8))
    msg = str(x3) + "," + str(y3)
    publish.single("ee2405/id3", msg, hostname=host_id)
    time.sleep(.01)
    ii = cv2.circle(ii, (x3, y3), 20, (0, 0, 255), -1)
    ### Magenta
    x4, y4 = getCoord(img, cv2.COLOR_BGR2HSV, np.array([165, 175, 160], np.uint8), np.array([175, 185, 185], np.uint8))
    msg = str(x4) + "," + str(y4)
    publish.single("ee2405/id4", msg, hostname=host_id)
    time.sleep(.01)
    ii = cv2.circle(ii, (x4, y4), 20, (0, 0, 255), -1)
    ## Orange 
    x5, y5 = getCoord(img, cv2.COLOR_BGR2RGB, np.array([190, 80, 35], np.uint8), np.array([205, 95, 55], np.uint8))
    msg = "car1_{0}_{1}_car2_{2}_{3}_car3_{4}_{5}_car4_{6}_{7}_car5_{8}_{9}".format(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5)
    publish.single("ee2405/id5", msg, hostname=host_id)
    ii = cv2.circle(ii, (x5, y5), 20, (0, 0, 255), -1)
    cv2.imwrite('i.jpg', ii)
    time.sleep(.01)
    time.sleep(1.5)
    if cnt % 10 != 0:
        cnt += 1
    else:
        cnt = 1
        cv2.imwrite('i.jpg', ii)
        html_str = """
        <html lang="en">
        <body>
            <h1>Hello, world!</h1>
            <img src="./i.jpg" height="300" >
            <p>
            <h1>id1</h1>
            <h3>{},{}</h3>
            </p>
            <p>
                <h1>id2</h1>
                <h3>{},{}</h3>
            </p>
            <p>
                <h1>id3</h1>
                <h3>{},{}</h3>
            </p>
            <p>
                <h1>id4</h1>
                <h3>{},{}</h3>
            </p>
            <p>
                <h1>id5</h1>
                <h3>{},{}</h3>
            </p>
        </body>
        </html>
        """
        #with open("a.html", "w") as f:
        #    f.write(html_str.format(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5))
        #browser.refresh()
#end listening
client.loop_stop()
