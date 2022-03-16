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
from utime import ticks_us, ticks_diff, sleep_us

posyPin = 0
negyPin = 0
posxPin = 0
negxPin = 0

class Touch:
    def __init__(self, XpPin, XmPin, YpPin, YmPin ,width, length, period):
        '''!@brief      initialize the touch panel.
            @param      XpPin defines the positive x pin for the touch panel.
            @param      XmPin defines the negative x pin for the touch panel.
            @param      YpPin defines the positive y pin for the touch panel.
            @param      YmPin defines the negative y pin for the touch panel.
        '''
        global posyPin, negyPin, posxPin, negxPin
        
        ## @brief set Xp equal to the passed in paramter for the postive x pin of the touch panel.
        self.Xp = XpPin
        
        ## @brief set Xm equal to the passed in paramter for the negative x pin of the touch panel.
        self.Xm = XmPin
        
        ## @brief set Yp equal to the passed in paramter for the postive y pin of the touch panel.
        self.Yp = YpPin
        
        ## @brief set Ym equal to the passed in paramter for the negative y pin of the touch panel.
        self.Ym = YmPin
        
        # Initial Setup for zScan
        posyPin = Pin(self.Yp, Pin.OUT_PP)
        negyPin = Pin(self.Ym, Pin.IN)
        posxPin = ADC(self.Xp)
        negxPin = Pin(self.Xm, Pin.OUT_PP)
        
        ## @brief width of the touch panel in mm.
        self.width = width
        
        ## @brief length of the touch panel in mm.
        self.length = length
        
        ## @brief period for reading values from the touch panel.
        self.period = period
        
        # Calibration Coefficients
        
        ## @brief calibration coefficient
        self.Kxx = 0
        
        ## @brief calibration coefficient
        self.Kxy = 0
        
        ## @brief calibration coefficient
        self.Kyx = 0
        
        ## @brief calibration coefficient
        self.Kyy = 0
        
        ## @brief calibration coefficient
        self.x0 = 0
        
        ## @brief calibration coefficient
        self.y0 = 0
        
        ## @brief previous x postion, used to calculate velocity.
        self.lastX = 0
        
        ## @brief previous y position, used to calculate velocity.
        self.lastY = 0
        
        
    def xScan(self):
        '''!@brief      Scan touch panel in x direction.
        '''
        global posyPin, negyPin, posxPin, negxPin
        
        posxPin = Pin(self.Xp, Pin.OUT_PP)
        posyPin = ADC(self.Yp)
        
        negxPin.low()
        posxPin.high()
        
        Vx = posyPin.read()
        
        #conversion into x
        x = ((Vx/4096)*self.length)-(self.length/2)
        
        return x
    
    
    def yScan(self):
        '''!@brief      Scan touch panel in y direction.
        '''
        global posyPin, negyPin, posxPin, negxPin
        
        posyPin = Pin(self.Yp, Pin.OUT_PP)
        negyPin = Pin(self.Ym, Pin.OUT_PP)
        posxPin = ADC(self.Xp)
        negxPin = Pin(self.Xm, Pin.IN)
        
        negyPin.low()
        posyPin.high()
        
        Vy = posxPin.read()
        
        #conversion into x
        y = ((Vy/4096)*self.width)-(self.width/2)
        
        return y
    
    
    def zScan(self):
        '''!@brief      Scan touch panel in z direction.
            @details    Determines if the ball is touching the platform.
        '''
        global posyPin, negyPin, posxPin, negxPin
        
        negyPin = Pin(self.Ym, Pin.IN)
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
    
        
    def touchFilter(self, num):
        '''!@brief      Filter the results from the touch panel.
            @details    Filters by taking the median of several measurements.
        '''
        # Take measurements and return the median
        xList = num*[0]
        yList = num*[0]
        for i in range(0,num):
            # Check if ball is touching
            z = self.zScan()
            
            # If ball is touching, update position and velocity
            if z:
                # Update position
                x = self.xScan()
                y = self.yScan()
                
                x = self.Kxx*x + self.Kxy*y + self.x0
                y = self.Kyy*y + self.Kyx*x + self.y0
                
                xList[i] = x
                yList[i] = y
                
            else:
                xList[i] = self.lastX
                yList[i] = self.lastY
                
        return numpy.median(numpy.ndarray(xList)), numpy.median(numpy.ndarray(yList))
    
    
    def update(self, num):
        # Check if ball is touching
        z = self.zScan()

        # If ball is touching, update position and velocity
        if z:
            '''# Update position
            x = self.xScan()
            y = self.yScan()
            
            x = self.Kxx*x + self.Kxy*y + self.x0
            y = self.Kyy*y + self.Kyx*x + self.y0'''
            
            x,y = self.touchFilter(num)
            
            #print(f"({x}, {y})")
            
            # Update velocity
            vX = (10**6)*(x-self.lastX)/self.period
            vY = (10**6)*(y-self.lastY)/self.period
            
            # Get rid of wonky velocity values
            if (abs(vX) > 1000) or (abs(vY) > 1000):
                vX, vY = 0, 0
            
            #print(f"({vX}, {vY})")
            
            self.lastX = x
            self.lastY = y
            
            return x, y, z, vX, vY
        
        # If ball is not touching, ignore stuff
        else:
            return 0, 0, z, 0, 0
        
    def calibrate(self):
        '''!@brief      Calibrate the touch panel.
            @details    Calibrates for scale, offset, skew.
        '''
        
        print("Please touch the top left dot.")
        while self.zScan() is False:
            # Do nothing
            pass
        
        x1 = self.xScan()
        y1 = self.yScan()
        
        
        print("Please remove finger.")
        while self.zScan() is True:
            # Do nothing
            pass
        
        print("Please touch bottom left dot.")
        while self.zScan() is False:
            # Do nothing
            pass
        
        x4 = self.xScan()
        y4 = self.yScan()
        
        print("Please remove finger.")
        while self.zScan() is True:
            # Do nothing
            pass
        
        print("Touch center.")
        while self.zScan() is False:
            # Do nothing
            pass
        
        x2 = self.xScan()
        y2 = self.yScan()
        
        print("Please remove finger.")
        while self.zScan() is True:
            # Do nothing
            pass
        
        print("Please touch top right dot.")
        while self.zScan() is False:
            # Do nothing
            pass
        
        x5 = self.xScan()
        y5 = self.yScan()
        
        print("Please remove finger.")
        while self.zScan() is True:
            # Do nothing
            pass
        
        print("Please touch bottom right dot.")
        while self.zScan() is False:
            # Do nothing
            pass
        
        x3 = self.xScan()
        y3 = self.yScan()
        
        
        # Create X matrix
        #data = f"{x1} {y1};{x2} {y2};{x3} {y3}"
        #X = numpy.matrix(data)
        X = numpy.array([[x1, y1, 1], [x2, y2, 1], [x3, y3, 1], [x4, y4, 1], [x5, y5, 1]])
        
        # Create Y matrix
        #data = "-80 40;0 0;80 -40"
        #Y = numpy.matrix(data)
        Y = numpy.array([[-80, 40], [0, 0], [80, -40], [-80, -40], [80, 40]])
        
        # Calculate B
        Xt = X.transpose()
        inv = numpy.linalg.inv(numpy.dot(Xt,X))
        combined = numpy.dot(Xt,Y)
        B = numpy.dot(inv,combined)
        
        self.Kxx = B[0][0]
        self.Kyx = B[0][1]
        self.Kxy = B[1][0]
        self.Kyy = B[1][1]
        self.x0 = B[2][0]
        self.y0 = B[2][1]
        
        
        myLine = f"{self.Kxx}, {self.Kyx}, {self.Kxy}, {self.Kyy}, {self.x0}, {self.y0}"
        
        # Check if file already exists, clear it and make a new one
        if 'touch_cal_coeffs.txt' in os.listdir():
            os.remove('touch_cal_coeffs.txt')
            
        with open("touch_cal_coeffs.txt", 'w') as file:
            file.write(myLine)
        
        print("Fully Calibrated!")
        
    
    def readCalibration(self):
        '''!@brief      read the calibration file if existing.
        '''
        with open("touch_cal_coeffs.txt", 'r') as file:
            data = file.readline()
        
        # Format Data
        data = data.split(', ')

        # Write each value to the IMU
        self.Kxx = float(data[0])
        self.Kyx = float(data[1])
        self.Kxy = float(data[2])
        self.Kyy = float(data[3])
        self.x0 = float(data[4])
        self.y0 = float(data[5])
            
        print("Device Calibrated")
    
    def checkCal(self):
        '''!@brief      Checks if a calibration file exists.
        '''
        # If a calibration file is detected, read from it
        if 'touch_cal_coeffs.txt' in os.listdir():
            #os.remove('touch_cal_coeffs.txt')
            self.readCalibration()
        # If no file is detected, make one
        else:
            self.calibrate()
    

if __name__ == "__main__":
    location = Touch(Pin.cpu.A7,Pin.cpu.A1,Pin.cpu.A6,Pin.cpu.A0,188,100, 10000)
    
    #location.calibrate()
    
    #print(f"{location.xCal}, {location.yCal}")
   
    timerStart = ticks_us()
        
    for i in range(0,1000):
        if location.zScan():
            location.xScan()
            location.yScan()
    
    current = ticks_us()
    print(f"Average time per XYZ scan: {ticks_diff(current,  timerStart)/1000} uSeconds")
    
    timerStart = ticks_us()
        
    for i in range(0,1000):
        location.update()
    
    current = ticks_us()
    print(f"Average time per Update: {ticks_diff(current,  timerStart)/1000} uSeconds")
    
    
    #while True:
       #print (location.update())
        # if location.zScan() > 0.01:
         #   print (location.xScan(), location.yScan())
        
            