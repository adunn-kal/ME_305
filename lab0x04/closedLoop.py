'''!@file    controlLoop.py
    @brief   Lab0x04 control loop.
    @details 
    @author  Emma Jacobs
    @author  Alexander Dunn
    @date    February 03, 2022
'''

class ClosedLoop:
    '''!@brief      Closed loop control of DC motor speed.
    '''
    
    def __init__(self):
        '''!@brief      Initialize the gain and duty.
        '''
        self.gain = 0
        self.max = 100
        self.min = -100
        self.duty = 0
        self.ref = 0
        
    def run(self, speed):
        '''!@brief      Use feedback to set the duty cycle.
            @param      speed retrieves the velocity from taskUser and uses it as feedback.
        '''
        self.speed = speed
        
        error = self.ref - self.speed
        
        duty = self.gain*(error)

        
        if duty > self.max:
            duty = self.max
        elif duty < self.min:
            duty = self.min
            
        self.duty = duty
        
        return duty
    
    def set_Kp(self, gain):
        '''!@brief     Set the gain.
            @param     Set the gain to what is specified in taskUser.
        '''
        self.gain = gain
        
