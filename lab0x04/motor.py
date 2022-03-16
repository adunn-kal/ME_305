'''!@file       motor.py
    @brief      Initialize a motor object and control it.
    @details    Set the duty cycle of the motor.
'''
from pyb import Pin, Timer

class Motor:
    '''!@brief      Defines a motor object.
        @details    Duty cycle can be set using ref/ set_duty().
    '''
    
    def __init__(self, PWM_time, IN1_pin, IN2_pin, ch1, ch2):
        '''!@brief      Intializes the motor object.
            @param      PWM_time The timer for the motor.
            @param      IN1_pin moves the motor forward.
            @param      IN2_pin moves the motor backwards.
            @param      ch1 channel 1 for forward movement.
            @param      Ch2 channel 2 for backward movement.
        '''
        ## @brief sets the pin to move the motor forward.
        self.forwardPin = IN1_pin
        
        ## @brief sets the pin to move the motor backwards.
        self.backPin = IN2_pin
        
        ## @brief sets the duty cycle based on closed loop control.
        self.duty = 0
        
        ## @brief enables PWM control on the forward pin.
        self.PWMforward = PWM_time.channel(ch1, Timer.PWM_INVERTED, pin=self.forwardPin)
        
        ## @brief enables PWM control of the back pin.
        self.PWMback = PWM_time.channel(ch2, Timer.PWM_INVERTED, pin=self.backPin)
                
    def set_duty(self, duty):
        '''!@brief      Set the duty cycle of the motor object.
            @param      duty define what the duty cycle value is, ranges from -100 to 100.
        '''
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
            
    