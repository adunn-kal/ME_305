from pyb import Pin, Timer

class Motor:
    '''!@brief      Defines a motor.
        @details    Duty cycle can be set using ref/ set_duty().
    '''
    
    def __init__(self, PWM_time, IN1_pin, IN2_pin, ch1, ch2):
        self.forwardPin = IN1_pin
        self.backPin = IN2_pin
        self.duty = 0
        self.PWMforward = PWM_time.channel(ch1, Timer.PWM_INVERTED, pin=self.forwardPin)
        self.PWMback = PWM_time.channel(ch2, Timer.PWM_INVERTED, pin=self.backPin)
                
    def set_duty(self, duty):
        '''!@brief      Set the duty cycle of the motor object.
            @param      duty define what the duty cycle value is, ranges from -100 to 100.
        '''
        print(f"Setting duty to {duty}%")
        self.duty = duty
        
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
            
            #IN1_pin = Pin(Pin.cpu.B4, mode=Pin.OUT_PP)
            #IN2_pin = Pin(Pin.cpu.B5, mode=Pin.OUT_PP)
            
            motor_1 = Motor(PWM_time, Pin.cpu.B4, Pin.cpu.B5, 1, 2)
            motor_2 = Motor(PWM_time, Pin.cpu.B0, Pin.cpu.B1, 3, 4)
            
            nSLEEP = Pin(Pin.cpu.A15, mode=Pin.OUT_PP)
            nSLEEP.high()
            
            motor_1.set_duty(0)
            motor_2.set_duty(-70)
            
        except KeyboardInterrupt:
            nSLEEP.low()
            print('sleep low')
            break
            
    