from pyb import Pin, Timer

class Motor:
    
    def __init__(self, PWM_time, IN1_pin, IN2_pin):
        self.forwardPin = IN1_pin
        self.backPin = IN2_pin
        
        
        self.PWMforward = PWM_time.channel(1, Timer.PWM_INVERTED, pin=self.forwardPin)
        self.PWMback = PWM_time.channel(2, Timer.PWM_INVERTED, pin=self.backPin)
                
    def set_duty(self, duty):
        
        if duty > 0:
            self.PWMforward.pulse_width_percent(0)
            self.PWMback.pulse_width_percent(duty)

        else:
            self.PWMforward.pulse_width_percent(-1*duty)
            self.PWMback.pulse_width_percent(0)
                   
        
    
if __name__ == '__main__':
    
    while True:
        try:
            PWM_time = Timer(3, freq = 20000)
            
         #   IN1_pin = Pin(Pin.cpu.B4, mode=Pin.OUT_PP)
         #  IN2_pin = Pin(Pin.cpu.B5, mode=Pin.OUT_PP)
            
            motor_1 = Motor(PWM_time, Pin.cpu.B4, Pin.cpu.B5)
            
            nSLEEP = Pin(Pin.cpu.A15, mode=Pin.OUT_PP)
            nSLEEP.high()
            
            motor_1.set_duty(80)
            
        except KeyboardInterrupt:
            nSLEEP.low()
            print('sleep low')
            break
            
    
        