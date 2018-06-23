#ifndef PARALLAX_STDSERVO_H
#define PARALLAX_STDSERVO_H

class parallax_stdservo {
    public:
        parallax_stdservo( PwmOut& input ) {
            dio = &input;
            dio->period(.02);
        }
        void write( int value ){
            int pwm_ms = (value)*750/90+1500;
            dio->write(pwm_ms/20000.0f);
        }
        int operator=( int value ){ write(value); return 1; }

    private:
        PwmOut *dio;
};
#endif


