#ifndef PARALLAX_SERVO_H
#define PARALLAX_SERVO_H
#include "mbed.h"
Ticker encoder_ticker;
class parallax_encoder;
std::vector<parallax_encoder*> encoder_list;
class parallax_encoder {
    public:
        parallax_encoder( DigitalIn& input ) {
            din = &input;
            steps = 0;
            last = 0;
            encoder_list.push_back(this);
        }
        void proc(){
            int value = din->read();
            if(!last && value) steps++;
            last = value;
        }
        int get_steps(){ return steps; }
        float get_cm(){ return get_steps()*6.5*3.14/32; }
        void reset(){ steps = 0; }
        operator int(){ return steps; }
    private:
        int steps;
        int last;
        DigitalIn *din;
};

//int encoder_list_num = 0;
void encoder_control(){
    int i;
    for( i=0; i<encoder_list.size(); i++ ){
        (encoder_list[i])->proc();
    }
}

#endif