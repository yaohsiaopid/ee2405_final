#include "bbcar.h"
extern parallax_servo *servo0_ptr, *servo1_ptr;
extern parallax_stdservo *claw0_ptr, *claw1_ptr;
extern parallax_ping *ping_ptr;
extern Ticker servo_ticker;

void bbcar_init( PwmOut &pin_servo0, PwmOut &pin_servo1, PwmOut &pin_claw0, PwmOut &pin_claw1, DigitalInOut &pin_ping){
    static parallax_servo servo0(pin_servo0);
    static parallax_servo servo1(pin_servo1);
    static parallax_stdservo claw0(pin_claw0);
    static parallax_stdservo claw1(pin_claw1);
    static parallax_ping ping(pin_ping);
    servo0_ptr = &servo0;
    servo1_ptr = &servo1;
    claw0_ptr = &claw0;
    claw1_ptr = &claw1;
    ping_ptr = &ping;
    servo_ticker.attach(&servo_control, .5);
    servo0 = 0; servo1 = 0;
}

void ServoStop( int speed ){
    servo0_ptr->set_speed(0);
    servo1_ptr->set_speed(0);
    servo0_ptr->set_factor(1);
    servo1_ptr->set_factor(1);
    return;
}

void ServoCtrl( int speed ){
    servo0_ptr->set_speed(speed);
    servo1_ptr->set_speed(-speed);
    return;
}

void ServoTurn( int speed, double turn ){
    static int last_speed = 0;
    if(last_speed!=speed){
        servo0_ptr->set_speed(speed);
        servo1_ptr->set_speed(-speed);
    }
    if(turn>0){
        servo0_ptr->set_factor(turn);
        servo1_ptr->set_factor(1);
    }
    if(turn<0){
        servo0_ptr->set_factor(1);
        servo1_ptr->set_factor(-turn);
    }
    return;
}

float global_kp, global_ki;
inline float clamp( float value, float max, float min ){ return (max<value)?max:((min>value)?min:value); }

void setController( float kp, float ki ){ global_kp = kp; global_ki = ki;}
inline int turn2speed( float turn ){ return 25+abs(25*turn); }
void controller( float err ){
    static float erri = 0;
    const float bound = .9;
    erri += err;
    float correction = err*global_kp + erri*global_ki;
    correction = clamp(correction, bound, -bound);
    printf("correction(%.2f,%.2f) = %3.2f (kp = %.2f, ki = %.2f)\r\n", err, erri, correction, global_kp, global_ki);
    float turn = ((correction>0) ?1:(-1)) - correction;
    ServoTurn(turn2speed(turn),turn);
}

