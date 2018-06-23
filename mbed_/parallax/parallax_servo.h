#ifndef PARALLAX_SERVO_H
#define PARALLAX_SERVO_H

#include "mbed.h"
#include <vector>

#define CENTER_BASE 1500

class parallax_servo;
extern Ticker servo_ticker;
extern std::vector<parallax_servo*> servo_list;
int truncate( int a, int b, int ramp );

class parallax_servo {
    public:
        parallax_servo(PwmOut& pin) {
            pin.period(.02);
            pwm = &pin;
            factor = 1;
            last = 0;
            ramp = 1500;
            goal = 1500;
            servo_list.push_back(this);
        }

        void servo_control(){
            last = truncate(last,goal,ramp);
            pwm->write((CENTER_BASE + (factor*last)) / 20000.0f);
        }

        void set_speed( int value ){
            goal = value;
        }
        void set_ramp( int value ){
            ramp = value;
        }
        void set_factor( double value ){
            factor = value;
        }

        int operator=( int value ){ set_speed(value); return 1; }

    private:
        PwmOut *pwm;
        double factor;
        int last;
        int goal;
        int ramp;
};


void servo_control();
int truncate( int a, int b, int ramp );
#endif
