#include "mbed.h"
#include "parallax.h"
#include "bbcar.h"
#include "bbcar_rpc.h"
#include "mbed_rpc.h"
#include "uLCD_4DGL.h"
#include <string>
#include <cmath>
#define PI 3.14159265
Serial pc(USBTX, USBRX);
DigitalOut led1(LED1);
PwmOut pin12(D11), pin11(D12), buzzer(D3), pin13(D13), pin7(D7);
DigitalInOut pin4(D4);
// uLCD_4DGL uLCD(D1, D0, D2);
parallax_servo *servo0_ptr, *servo1_ptr;
parallax_stdservo *claw0_ptr, *claw1_ptr;
parallax_ping *ping_ptr;

void claw_ops();
void ServoStopForce();
void init_claw();
void StopCar(Arguments *in, Reply *out);
void ScoopOp(Arguments *in, Reply *out);
void UTurn(Arguments *in, Reply *out);
RPCFunction rpcScoopOp(&ScoopOp, "ScoopOp"); 
RPCFunction rpcStopCar(&StopCar, "StopCar");
RPCFunction rpcUTurn(&UTurn, "UTurn");
// cmd = "/UTurn/run 0 1\n"
float wt = 1.6;
int main() {
    
       
    bbcar_init(pin11, pin12, pin13, pin7, pin4);

    init_claw();
    // *servo0_ptr = -60;
    // *servo1_ptr = -60;
    // wait(wt);
    // ServoStopForce();
   
    // ScoopOp(1);
    // UTurn(0,0);
    // wait(0.5);
    
    // ScoopOp(0,0);
    // uLCD.printf("jjjj");
    pc.baud(9600);
    char buf[256], outbuf[256];
    while (1) {
        int i;
        for( i=0; ;i++ ) {
            buf[i] = pc.getc();
            if(buf[i] == '\n') break;
        }
        if(buf[0] != '/') {
            // uLCD.cls();
            // uLCD.printf("%s\n", buf);
            // int j = 0;
            // while(buf[j] != '|') { uLCD.printf("%c", buf[j]); j++; }
            // j++;
            // uLCD.printf("\n");
            // while(buf[j] != '\n' && j < i) { uLCD.printf("%c", buf[j]); j++;}
            
        } else {
            RPC::call(buf, outbuf);
        }
        
        // pc.printf("%s\r\n", outbuf);
    }
    return 0;
}

void init_claw()
{
    *claw1_ptr = -110;
    *claw0_ptr = -20;
}
void claw_ops()
{
    *claw0_ptr = 50;
    wait(3);
    *claw1_ptr = 30;
    wait(3);
    *claw0_ptr = -20;
    wait(0.5);
    *claw1_ptr = -115;
}

void ServoStopForce(){
    servo0_ptr->set_speed(0);
    servo1_ptr->set_speed(0);
    servo0_ptr->servo_control();
    servo1_ptr->servo_control();
}
void StopCar(Arguments *in, Reply *out)
{
    // pc.printf("stopppp");
    ServoStopForce();
}


// after stop at red, scoop
void ScoopOp(Arguments *in, Reply *out)
{
    int r = in->getArg<int>();
    wait(1);
    *servo0_ptr = 85;
    *servo1_ptr = -55;
    float dis = 1000;
    while(dis > 5) {
        dis = (float)(*ping_ptr);
        wait(0.01);
    }
    ServoStopForce();
    wait(0.5);

    
    // int r = 0;
    // 0 one time
    init_claw();    
    *servo0_ptr = -60;
    *servo1_ptr = -60;
    wait(wt);
    ServoStopForce();
    wait(2);
    claw_ops();
    
    *servo0_ptr = -60;
    *servo1_ptr = -60;
    wait(wt);
    ServoStopForce();
    wait(1);
    *claw0_ptr = 35;
 
    wait(2);
    if(r == 1) {
        init_claw();
        *servo0_ptr = 60;
        *servo1_ptr = 60;
        wait(wt);
        ServoStopForce();
        wait(2);
        claw_ops();
        
        *servo0_ptr = -60;
        *servo1_ptr = -60;
        wait(wt);
        ServoStopForce();
        wait(1);
        *claw0_ptr = 35;
    }
    wait(2);
    *claw1_ptr = 30; // put down the arm
    wait(1);
    *claw1_ptr = 50;
    
    // *servo0_ptr = 65;
    // *servo1_ptr = 65;
    // wait(1.1);
    // ServoStopForce();
    // wait(1);
    // *servo0_ptr = 55;
    // *servo1_ptr = -75;
    // wait(1.2);
    // ServoStopForce();

    pc.printf("d");

}

void UTurn(Arguments *in, Reply *out)
{   
    
    // init_claw();
    *claw0_ptr = 50;
    *claw1_ptr = -110;
    wait(0.5);
    *servo0_ptr = 65;
    // *servo1_ptr = -95;
    wait(1.5);
    ServoStopForce();
    wait(0.5);
    pc.printf("ojjjjiiii");
}