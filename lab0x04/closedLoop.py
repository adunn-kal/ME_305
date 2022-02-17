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
        self.duty = 0
        
    def run(self, ref, speed):
        self.ref = ref
        self.speed = speed
        step = 25
        
        error = self.ref - self.speed
        
        duty = self.gain*(error)
        
        '''if (duty - self.duty) > step:
            duty = self.duty + step
        elif (self.duty - duty) > 25:
            duty = self.duty - 25
        '''
        
        if duty > self.max:
            duty = self.max
        elif duty < self.min:
            duty = self.min
            
        self.duty = duty
            
        print(error)
        print(duty)
        
        return duty
    
    def set_Kp(self, gain):
        self.gain = gain
        
