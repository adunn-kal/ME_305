'''!@file    closedLoop.py
    @brief   Lab0x04 control loop.
    @details 
    @author  Emma Jacobs
    @author  Alexander Dunn
    @date    February 03, 2022
'''

class ClosedLoop:
    
    def __init__(self):
        self.Kp = 0
        self.Kd = 0
        self.max = 30
        self.duty_x = 0
        self.duty_y = 0
        self.ref = 0
        
    def run(self, roll, pitch, Vx, Vy):        
        duty_x = -self.Kp*(roll) - self.Kd*(Vx)
        
        duty_y = -self.Kp*(pitch) - self.Kd*(Vy)

        
        if duty_x > self.max:
            duty_x = self.max
        elif duty_x < -self.max:
            duty_x = -self.max
            
        if duty_y > self.max:
            duty_y = self.max
        elif duty_y < -self.max:
            duty_y = -self.max
            
        self.duty_x = duty_x
        self.duty_y = -duty_y
        
        return [self.duty_x, self.duty_y]
    
    def set_Kp(self, gain):
        self.Kp = gain
        
    def set_Kd(self, gain):
        self.Kd = gain
        
