'''!@file    closedLoop.py
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
        
        ## @brief shows the relationship between the magnitude of the input to
        #         the magnitude of the output signal for velocity.
        self.Kp = 0
        
        ## @brief shows the relationship between the magnitude of the input to
        #         the magnitude of the output signal for position.
        self.Kd = 0
        
        ## @brief max limits the maximum duty cycle.
        self.max = 100
        
        ## @brief specifies the duty of the motor for the x direction.
        self.duty_x = 0
        
        ## @brief specifies the duty of the motor for the y direction.
        self.duty_y = 0
        
        ## @brief ref retrieves the reference velocity as defined earlier.
        self.ref = 0
        
    def setMax(self, maximum):
        '''!@brief      Set the maximum, used in the duty cycle,
        '''
        
        self.max = maximum
        
    def run(self, x, y, Vx, Vy, xRef, yRef): 
        '''!@brief      Use feedback to set the duty cycle.
            @param      x measured x position.
            @param      y measured y position.
            @param      Vx measured x velocity.
            @param      Vy measured y velocity.
            @param      xRef x reference position.
            @param      yRef y reference position.
        '''
        duty_x = self.Kp*(xRef - x) - self.Kd*(Vx)
        
        duty_y = self.Kp*(yRef - y) - self.Kd*(Vy)

        if xRef != 0:
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
        '''!@brief      Sets Kp equal to gain.
            @param      Kp gain.
        '''
        self.Kp = gain
        
    def set_Kd(self, gain):
        '''!@brief      Sets Kd equal to gain.
            @param      Kd gain.
        '''
        self.Kd = gain
        
