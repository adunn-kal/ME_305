'''!@file    Touch.py
    @brief   Lab0x06 platform touchscreen control.
    @details 
    @author  Emma Jacobs
    @author  Alexander Dunn
    @date    March 3, 2022
'''
from pyb import Pin, ADC
from utime import ticks_us, ticks_diff, sleep_us

class Touch:
    def __init__(self, XpPin, XmPin, YpPin, YmPin ,width, length):
        self.Xp = XpPin
        self.Xm = XmPin
        self.Yp = YpPin
        self.Ym = YmPin
        
        self.width = width
        self.length = length
        
        self.xCal = 0
        self.yCal = 0
        
        
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
        z = self.zScan()
        if z:
            sleep_us(4)
            x = self.xScan()
            sleep_us(4)
            y = self.yScan()
            
            return x,y,z
        else:
            return None, None, z
        
    def calibrate(self):
        self.xCal = 0
        self.yCal = 0
        
        print("Please touch the top left dot.")
        while self.zScan() is False:
            # Do nothing
            pass
        
        x1, y1, z = self.update()
        x1Offset = x1 + 80
        y1Offset = y1 - 40
        
        
        print("Please remove finger.")
        while self.zScan() is True:
            # Do nothing
            pass
        
        
        print("Touch center.")
        while self.zScan() is False:
            # Do nothing
            pass
        
        x2Offset, y2Offset, z = self.update()
        
        
        print("Please remove finger.")
        while self.zScan() is True:
            # Do nothing
            pass
        
        
        print("Please touch bottom right dot.")
        while self.zScan() is False:
            # Do nothing
            pass
        
        x3, y3, z = self.update()
        x3Offset = x3 - 80
        y3Offset = y3 + 40
        
        
        # Get average offsets
        self.xCal = (x1Offset + x2Offset + x3Offset) / 3
        self.yCal = (y1Offset + y2Offset + y3Offset) / 3
        
        print("Fully Calibrated!")
    

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
        
            