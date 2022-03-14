'''!@file    Touch.py
    @brief   Lab0x06 platform touchscreen control.
    @details 
    @author  Emma Jacobs
    @author  Alexander Dunn
    @date    March 3, 2022
'''
from pyb import Pin, ADC
import os
from ulab import numpy
#from utime import ticks_us, ticks_diff, sleep_us

class Touch:
    def __init__(self, XpPin, XmPin, YpPin, YmPin ,width, length, period):
        self.Xp = XpPin
        self.Xm = XmPin
        self.Yp = YpPin
        self.Ym = YmPin
        
        self.width = width
        self.length = length
        self.period = period
        
        self.xCal = 0
        self.yCal = 0
        
        self.lastX = 0
        self.lastY = 0
        
        
    def xScan(self):
        posxPin = Pin(self.Xp, Pin.OUT_PP)
        negxPin = Pin(self.Xm, Pin.OUT_PP)
        posyPin = ADC(self.Yp)
        negyPin = Pin(self.Ym, Pin.IN)
        
        negxPin.low()
        posxPin.high()
        
        Vx = posyPin.read()
        
        #conversion into x
        x = ((Vx/4096)*self.length)-(self.length/2) - self.xCal
        
        return x
    
    
    def yScan(self):
        posyPin = Pin(self.Yp, Pin.OUT_PP)
        negyPin = Pin(self.Ym, Pin.OUT_PP)
        posxPin = ADC(self.Xp)
        negxPin = Pin(self.Xm, Pin.IN)
        
        negyPin.low()
        posyPin.high()
        
        Vy = posxPin.read()
        
        #conversion into x
        y = ((Vy/4096)*self.width)-(self.width/2) - self.yCal
        
        return y
    
    
    def zScan(self):
        posyPin = Pin(self.Yp, Pin.OUT_PP)
        negyPin = Pin(self.Ym, Pin.IN)
        posxPin = ADC(self.Xp)
        negxPin = Pin(self.Xm, Pin.OUT_PP)
        
        negxPin.low()
        posyPin.high()
        
        Vz = posxPin.read()
        
        #conversion into x
        z = (Vz/4096)
        
        if z > 0.01:
            return True
        else:
            return False
        
    def update(self):
        # Check if ball is touching
        z = self.zScan()
        
        # If ball is touching, update position and velocity
        if z:
            # Update position
            x = self.xScan()
            y = self.yScan()
            
            print(f"({x}, {y})")
            
            # Update velocity
            vX = (10**6)*(x-self.lastX)/self.period
            vY = (10**6)*(y-self.lastY)/self.period
            
            self.lastX = x
            self.lastY = y
            
            return x,y,z, vX, vY
        
        # If ball is not touching, ignore stuff
        else:
            return 0, 0, z, 0, 0
        
    def calibrate(self):
        self.xCal = 0
        self.yCal = 0
        
        print("Please touch the top left dot.")
        while self.zScan() is False:
            # Do nothing
            pass
        
        x1, y1, z = self.update()[0:3]
        
        
        print("Please remove finger.")
        while self.zScan() is True:
            # Do nothing
            pass
        
        
        print("Touch center.")
        while self.zScan() is False:
            # Do nothing
            pass
        
        x2, y2, z = self.update()[0:3]
        
        
        print("Please remove finger.")
        while self.zScan() is True:
            # Do nothing
            pass
        
        
        print("Please touch bottom right dot.")
        while self.zScan() is False:
            # Do nothing
            pass
        
        x3, y3, z = self.update()[0:3]
        
        
        # Create X matrix
        data = f"{x1} {y1};{x2} {y2};{x3} {y3}"
        X = numpy.matrix(data)
        
        # Create Y matrix
        data = "-80 40;0 0;80 -40"
        Y = numpy.matrix(data)
        
        # Calculate B
        Xt = numpy.transpose(X)
        inv = numpy.linalg.inv(numpy.multiply(Xt,X))
        combined = numpy.multiply(Xt,Y)
        B = numpy.multiply(inv,combined)
        print(B)
        
        
        myLine = ''
        myLine += str(self.xCal)
        myLine += ', '
        myLine += str(self.yCal)
        
        with open("touch_cal_coeffs.txt", 'w') as file:
            file.write(myLine)
        
        print("Fully Calibrated!")
        
    
    def updateCalibration(self):
        with open("touch_cal_coeffs.txt", 'r') as file:
            data = file.readline()
        
        # Format Data
        data = data.split(', ')

        # Write each value to the IMU
        self.xCal = int(data[0])
        self.yCal = int(data[1])
            
        print("Device Calibrated")
    
    def checkCal(self):
        # If a calibration file is detected, read from it
        if 'touch_cal_coeffs.txt' in os.listdir():
            #os.remove('touch_cal_coeffs.txt')
            self.updateCalibration()
        # If no file is detected, make one
        else:
            self.calibrate()
    

if __name__ == "__main__":
    location = Touch(Pin.cpu.A7,Pin.cpu.A1,Pin.cpu.A6,Pin.cpu.A0,188,100)
    
    location.calibrate()
    
    print(f"{location.xCal}, {location.yCal}")
    '''
    timerStart = ticks_us()
        
    for i in range(0,1000):
        if location.zScan():
            location.xScan()
            location.yScan()
    
    current = ticks_us()
    print(ticks_diff(current,  timerStart)/1000)
    
    timerStart = ticks_us()
        
    for i in range(0,1000):
        location.update()
    
    current = ticks_us()
    print(ticks_diff(current,  timerStart)/1000)
    '''
    
    #while True:
       #print (location.update())
        # if location.zScan() > 0.01:
         #   print (location.xScan(), location.yScan())
        
            