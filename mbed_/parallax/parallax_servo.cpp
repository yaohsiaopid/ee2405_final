#include "parallax_servo.h"
Ticker servo_ticker;
std::vector<parallax_servo*> servo_list;

void servo_control(){
    for( int i=0; i<servo_list.size(); i++ ){
        (servo_list[i])->servo_control();
    }
}

int truncate( int a, int b, int ramp ) {
    if (abs(a - b) < ramp) return b;
    else return (a > b) ? (a - ramp) : (a + ramp);
}

