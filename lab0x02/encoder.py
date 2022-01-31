'''!@file    encoder.py
    @brief   A driver for reading from Quadrature Encoders.
    @details The class that reports and records the position of the motor.
    @author  Alexander Dunn
    @author  Emma Jacobs
    @date    January 20, 2022
 '''
import pyb
 
pinB6 = pyb.Pin(pyb.Pin.cpu.B6)
pinB7 = pyb.Pin(pyb.Pin.cpu.B7)


class Encoder:
    '''!@brief    Interface with quadrature encoders.
        @details  Intializes an encoder object based on user inputs for pins
                  and timer.
                  Contains methods to update the position and reset it.
    '''
    
    def __init__(self, chA_pin, chB_pin, timNum):
        '''!@brief    Constructs an encoder object.
            @details  Intializes timer with channels and sets up initial
                      position.
        '''
        print('Creating encoder object')
        # Set up timer and channels
        self.timer = pyb.Timer(timNum, prescaler=0, period=65535)
        self.ch1 = self.timer.channel(1, pyb.Timer.ENC_AB, pin=chA_pin)
        self.ch2 = self.timer.channel(2, pyb.Timer.ENC_AB, pin=chB_pin)
        
        # Sets up initial position and differences
        self.position = 0
        self.dif = 0
        self.lastCount = 0
        self.dataList = []
    
    def update(self):
        '''!@brief    Updates encoder position and delta.
            @details  Computes a difference in ticks and adds that difference
                      to the position.
        '''
        count = self.timer.counter()
        dif = count - self.lastCount
        self.lastCount = count
        
        if dif >= ((65535+1)/2):
            dif -= (65535+1)
            self.dif = dif
            
        elif dif < -((65535+1)/2):
            dif += (65535+1)
            self.dif = dif
            
        else:
            self.dif = dif
        
        self.position += self.dif
      
    def get_position(self):
        '''!@brief    Returns encoder position.
            @return   The position of the encoder shaft.
        '''
        # Return the position
        return self.position
    
    def zero(self, position):
        '''!@brief Resets the encoder position to zero.
        '''
        # Reset the position to zero
        self.position = 0
        
    def get_delta(self):
        '''!@brief    Returns encoder delta.
            @details  Uses the difference computed in the update() method.
            @return   The change in position of the encoder shaft
                      between the two most recent updates.
        '''
        # Return the difference
        return self.dif
     
if __name__ == '__main__':
    # Create an encoder object
    encoder_1 = Encoder(pinB6, pinB7, 4) 
    
    # Loop forever printing positions
    while True:
        encoder_1.update() #update encoder 1
        print(encoder_1.get_position())