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
        ## @brief gain determines the contribution of the error to restoring forces proportional
        #         to the velocity of the platform.
        self.gain = 0
        
        ## @brief max limits the maximum duty cycle.
        self.max = 100
        
        ## @brief min limits the minimum duty cycle.
        self.min = -100
        
        ## @brief duty specifies the duty of the motors, has a maximum and minimum.
        self.duty = 0
        
        ## @brief ref retrieves the reference velocity as defined earlier.
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
    
    def set_Kp(self, gain): #check params
        '''!@brief     Set the gain.
            @param     gain Set the gain to what is specified in taskUser.
        '''
        self.gain = gain
        
