from motor import Motor
from pyb import Pin, Timer, ExtInt


class DRV8847:
    '''!
    '''
    def __init__(self, sleepPin, faultPin, timer):
        self.timer = Timer(timer, freq = 20000)
        self.sleepPin = Pin(sleepPin, mode=Pin.OUT_PP)
        self.faultPin = faultPin
        
    def enable(self):
        self.sleepPin.high()
    
    def disable(self):
        self.sleepPin.low()
        
    def fault_cb(self, IRQ_src):
        self.disable()
    
    def makeMotor(self, IN1_pin, IN2_pin, ch1, ch2):
        motor = Motor(self.timer, IN1_pin, IN2_pin, ch1, ch2)
        return motor

        
if __name__ == '__main__':
    while True:
        try:
            myDriver = DRV8847(Pin.cpu.A15, Pin.cpu.B2, 3)
            
            motor_1 = myDriver.makeMotor(Pin.cpu.B4, Pin.cpu.B5, 1, 2)
            motor_2 = myDriver.makeMotor(Pin.cpu.B0, Pin.cpu.B1, 3, 4)
            
            faultInt_1 = ExtInt(Pin.cpu.B2, mode=ExtInt.IRQ_RISING, pull=Pin.PULL_NONE, callback=motor_1.fault_cb)
            faultInt_2 = ExtInt(Pin.cpu.B2, mode=ExtInt.IRQ_RISING, pull=Pin.PULL_NONE, callback=motor_2.fault_cb)

            myDriver.enable()
            
            motor_1.set_duty(50)
            motor_2.set_duty(-70)
            
        except KeyboardInterrupt:
            myDriver.disable()
            print('Disabling motors')
            break