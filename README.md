# Mr.Bean's Packaging Line––packaging
Our team consists of five members, and we are making our robots to collaborate to achieve a packaginig line. There are five stages in our pakacging line: beans bucket(robot chooses the right beans bucket)->packaging(robot scoops from bucket of bean into individual package)->stacking(robot takes the individual packages onto pallets->send to warehouse(robot take sthe pallets to the right warehouse)->examiniation(the robot will take notification from control center to blame a robot)

I am responsible for packaging. My robot will first navigate to operation area(tagged by red line on the field) then read the picture on the individual package to decide how many scoops for this package(either 1 or 2). Then it scoops beans from the bucket(assuming put on the  side of the road). Next it will bring the package with beans to next transition area(indicated by control center by MQTT) to complete its job.

Collaborators : Chuan-Chia Chang, Thomas Chou, Ya-Ting Yang, Yi-Yu Cheng 


## Hardware
* Boe Bot Car 
* K64F
* Servo Motors * 2
* Standard Servo * 2
* Claw: Mechanics for scooping 
* Udoo Neo 
* Acess Point/Router
* Camera
* box of beans
* another box with picture on it

## Steps
1. Set up environment  
    - Assemble the Boe Bot car as shown below   
![Imgur](https://i.imgur.com/K66OMjy.jpg)   
![Imgur](https://i.imgur.com/URdE8fx.jpg)  

    - Set up a LAN with the wireless router   

2. Mbed  
The `mbed_` folder contains all the library and `main.cpp` that will be flashed into K64F board. 

The libarary we use:  
- bbcar control: the original library can not init other parallax class such as parallax_stdservo aside from parallax_servo, because the compiler will raise parallax_stdservo as undefined even I include it in the `bbcar.h`  
It turned out that the problem lies in `parallax` module. Only did `parallax_servo.h` has the `#ifndef` macro in it. So once we added `#ifndef` in other header files in parallax, the problem never raised again because the `#ifndef` will prevent library be included twice.   

- bbcar_rpc  

The `main.cpp` simply goes into a loop taking commands from serial after initiating the servos and the claw. Also, it includes some custom function for claw operations.

3. python script on udoo neo 
Udoo Neo is responsible to process the input information such as mqtt messages and input images and make commands to mbed controller for the motion in resopnse to the inputs. 
- Lane following:  
    * files(in `/py_`): `calibrate.py, color_show.py, draw_line.py, get_contours.py, select_contours.py, udoo_control_center.py`   
    * `calibrate.py`: do perspective transform to the raw image taken from camera installed on the bot. `transform_ratio` is the factor effecting the how much of the original border area is remained in the transformed image. The higher the ratio, the more original part in raw image is maintained.   
    * **color_show.py & draw_line.py**: The color_show.py presents the raw image in different color space for you to find the mask range for the yellow and white lines detection, which is implemented in draw_line.py . The draw_line first use `cv2.inRange(cvt, low, high)` to generate the binary mask for targeted line.  
    One important implementation is the dilation and erode after the program gets a binary mask. The sequnce of dilation and erode greatly attributes the effectiveness of the draw_line.py. If erosion comes *before* dilation, the effect is same as denoising the image first then amplifing the signal of the lines. But the downside is that denoising may also erodes away our targeted signal(ie the lines). Therefore, **dilation before erosion** brought a higher probability that the draw_line detects line with a trade off in line may be a little distorted in the direction because of dilation being the first operation.    

    At extreme experiemnt of mine, switching the sequecne of the two operation can leads to one complete reult in detecting all lines(red, yellow and white) compare to one total failure in outputting none of the lines under the condition of using the same image.   
    
    * `select_contours.py` & `get_contours.py`: They simply use functions such as findContours provided by openCV to get the contour of image and select a contour.  
    * `udoo_control_center`: 
        The are two methods relevant to openCV lane following: `nav_to_red` and `nav_to_trans`. Their difference lies in the condition of stopping the car.  
        Essentially, the method takes in raw image, calibrates it, and use the `get_contour_from_image` method to get the drivable area of the road. Specifically this method uses draw_line.py to obtain the lines of the road, get contours from images(ie the candidates of the drivable area of the road)), remove the contours on the left side of the yellow_line(assuming the bot is driving on the right lane of the road), and return the leftest one of the remaining contours as the drivable are of the car.

        Then this returned contour is inputed into `control` method to obtain the center of the contour and the control_vector of the car (which points from the middle of the bottom line of the image to center of the selected center). This vector will be put into _control_center for PID control of the two servo motors.

- keras trained model:   
    The images to be detected are on the individual package(or the box). The keras trained model will detect if the image contain pikachu(a cartoon character) or not. 
    Then the robot will scoop either one or two scoops of beans into this package.  
    
    Specifically, the model will be trained on computer using Keras(source files are in `img_rec/`), and then the network is converted into tensorflow's file format for udoo neo to infer with openCV.  

    The inference takes place in the keras_scoop method of `udoo_control_center.py`.
 
- wireless communication––MQTT center(`mqtt_center.py`):  
    As a broker of the interconnection network, it first set up the listening services and then put it in background so that when any robot connectting to the server can send message to the  control center. On the other hand, it will get raw image from bird view camera and then interpret each robot's location by the tags of different color put on them using cv2.inRange.  
    
- Other minor features:
    * update_bar: return status of this robot using mqtt publish  
    * scoop_ops(num):   
    After the network outputs the detection result, it will call a rpcfunction called ScoopOp defined in main.cpp of the mbed files. The ScoopOp contains the hard coded commands for scooping the beans out of the bucket then put into the package.    



## Other fun things we tried  
* Naive DDOS the Udoo Neo ?!: Only tried out using serveral PCs to `ping` one Udoo Neo (running mqtt center) simultaneously. Though it seemed that the receiving on the devices does have longer latency, it does no harm for the operation of the udoo neo, because this naive method only blow up the incoming packet of the wireless card on the udoo neo ? ?? 
* Thinking: The udoo-neo is simply too unstable because the power system quickly runs out of power because of usage of too mamy servos and the charged batteries as the power source.