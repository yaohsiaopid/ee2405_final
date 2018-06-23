#ifndef BBCAR_H
#define BBCAR_H
#include "parallax_servo.h"
#include "parallax_stdservo.h"
#include "parallax_ping.h"
// #include "parallax.h"
extern float global_kp, global_ki;
void bbcar_init( PwmOut &pin_servo0, PwmOut &pin_servo1, PwmOut &pin_claw0, PwmOut &pin_claw1,DigitalInOut &pin_ping);
void ServoStop( int speed );
void ServoCtrl( int speed );
void ServoTurn( int speed, double turn );
void Buzz();
void controller( float err );
void setController( float kp, float ki );

#endif
