from motor import Motor
from pyb import Pin, Timer, ExtInt
import time


class DRV8847:
    '''!
    '''
    def __init__(self, sleepPin, faultPin, timer):
        self.timer = Timer(timer, freq = 20000)
        self.sleepPin = Pin(sleepPin, mode=Pin.OUT_PP)
        self.faultPin = faultPin
        
        self.faultInt = ExtInt(self.faultPin, mode=ExtInt.IRQ_FALLING, pull=Pin.PULL_UP, callback=self.fault_cb)
        
    def enable(self):
        self.faultInt.disable()
        self.sleepPin.high()
        time.sleep_us(50)
        self.faultInt.enable()
    
    def disable(self):
        self.sleepPin.low()
        
    def fault_cb(self, IRQ_src):
        self.disable()
        print("triggered fault")
    
    def makeMotor(self, IN1_pin, IN2_pin, ch1, ch2):
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
        