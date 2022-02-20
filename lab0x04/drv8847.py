'''!@file       drv8847.py
    @brief      Driver for the motor class.
'''
from motor import Motor
from pyb import Pin, Timer, ExtInt
import time


class DRV8847:
    '''!@brief      Driver for motor objects.
        @details    Can create multiple motor objects and handles fault conditions.
    '''
    def __init__(self, sleepPin, faultPin, timer):
        '''!@brief      Initialize a motor.
            @param      sleepPin Turn the enable pin off so motor cannot spin.
            @param      faultPin If a fault is tripped, disables the motor.
            @param      timer frequency of motor.
        '''
        self.timer = Timer(timer, freq = 20000)
        self.sleepPin = Pin(sleepPin, mode=Pin.OUT_PP)
        self.faultPin = faultPin
        
        self.faultInt = ExtInt(self.faultPin, mode=ExtInt.IRQ_FALLING, pull=Pin.PULL_UP, callback=self.fault_cb)
        self.fault = False
        
    def enable(self):
        '''!@brief      Disable the fault, set sleepPin to high.
        '''
        self.faultInt.disable()
        self.sleepPin.high()
        time.sleep_us(100)
        self.faultInt.enable()
        self.fault = False
    
    def disable(self):
        '''!@brief      Set sleepPin to low.
        '''
        self.sleepPin.low()
        self.fault = True
        
    def fault_cb(self, IRQ_src):
        '''!@brief      Disables motors if fault is triggered.
            @param      IRQ_src The interuppt parameter that indicates a fault.
        '''
        self.disable()
        print("triggered fault")
    
    def makeMotor(self, IN1_pin, IN2_pin, ch1, ch2):
        '''!@brief      Creates a motor object.
            @param      IN1_pin moves the motor forward.
            @param      IN2_pin moves the motor backwards.
            @param      ch1 channel 1 for forward movement.
            @param      Ch2 channel 2 for backward movement.
        '''
        motor = Motor(self.timer, IN1_pin, IN2_pin, ch1, ch2)
        return motor

        
if __name__ == '__main__':
    myDriver = DRV8847(Pin.cpu.A15, Pin.cpu.B2, 3) 
    print("Starting")
    
    motor_1 = myDriver.makeMotor(Pin.cpu.B4, Pin.cpu.B5, 1, 2)
    motor_2 = myDriver.makeMotor(Pin.cpu.B0, Pin.cpu.B1, 3, 4)
    

    myDriver.enable()
    
    
    while True:
        try:
            motor_1.set_duty(50)
            motor_2.set_duty(-70)
            
        except KeyboardInterrupt:
            myDriver.disable()
            print('Disabling motors')
            break
        