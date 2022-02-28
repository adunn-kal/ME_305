'''!@file    controlLoop.py
    @brief   Lab0x04 control loop.
    @details 
    @author  Emma Jacobs
    @author  Alexander Dunn
    @date    February 03, 2022
'''

class ClosedLoop:
    
    def __init__(self):
        self.gain = 0
        self.max = 100
        self.min = -100
        self.duty_x = 0
        self.duty_y = 0
        self.ref = 0
        
    def run(self, roll, pitch):        
        error_x = 0 - roll
        duty_x = self.gain*(error_x)
        
        error_y = 0 - pitch
        duty_y = self.gain*(error_y)

        
        if duty_x > self.max:
            duty_x = self.max
        elif duty_x < self.min:
            duty_x = self.min
            
        if duty_y > self.max:
            duty_y = self.max
        elif duty_y < self.min:
            duty_y = self.min
            
        self.duty_x = duty_x
        self.duty_y = -duty_y
        
        return [self.duty_x, self.duty_y]
    
    def set_Kp(self, gain):
        self.gain = gain
        
