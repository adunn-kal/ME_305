'''!@file    closedLoop.py
    @brief   Creates a control loop, used for both inner and outer loop.
    @details Runs PD control.
    @author  Emma Jacobs
    @author  Alexander Dunn
    @date    March 18, 2022
'''

class ClosedLoop:
    '''!@brief      Closed loop control for both inner and outer loops.
        @details    Inner loop: takes reference angular position and compares to measured 
                    angular position and velocity to set duty cycles for motors.
                    Outer loop: takes reference linear position and compares to measured 
                            linear position and velocity to set ref angular position
                            for inner loop.
    '''
    
    def __init__(self):
        '''!@brief      Initialize the loop.
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
        '''!@brief      Set the maximum saturation point.
        '''
        self.max = maximum
        
    def run(self, x, y, Vx, Vy, xRef, yRef): 
        '''!@brief      Use feedback to set the duty cycle.
            @param      x measured x angular or linear position.
            @param      y measured y angular or linear position.
            @param      Vx measured x angular or linear velocity.
            @param      Vy measured y angular or linear velocity.
            @param      xRef x reference angular or linear position.
            @param      yRef y reference angular or linear position.
            @return     x and y reference position or duty.
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
        '''!@brief      Updates Kp.
            @param      Kp gain.
        '''
        self.Kp = gain
        
    def set_Kd(self, gain):
        '''!@brief      Updates Kd.
            @param      Kd gain.
        '''
        self.Kd = gain
        
