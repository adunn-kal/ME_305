'''!@file    BNO055.py
    @brief   Lab0x05 IMU driver.
    @details 
    @author  Emma Jacobs
    @author  Alexander Dunn
    @date    February 24, 2022
'''
import pyb
import time
import struct

class BNO055:
    
    def __init__(self):
        self.imu = pyb.I2C(1, pyb.I2C.CONTROLLER)
        self.imu.mem_write(0b0000, 40, 0x3D)
        time.sleep_ms(20)
        
    def operatingMode(self):
        self.imu.mem_write(0b1000, 40, 0x3D)
        
    def calibration(self):
        calStat = self.imu.mem_read(1, 40, 0x35)[0]
        magStat = calStat & 0b00000011
        accStat = (calStat & 0b00001100) >> 2
        gyrStat = (calStat & 0b00110000) >> 4
        sysStat = (calStat & 0b11000000) >> 6
        
        return magStat, accStat, gyrStat, sysStat
    
    def getData(self):
        #check axis
        
        data = self.imu.mem_read(6, 40, 0x1A)
        heading, roll, pitch = struct.unpack('<hhh', data)
        
        return heading/16, roll/16, pitch/16
    
    def angularVelocity(self):
        pass
        
if __name__ == "__main__":
    myIMU = BNO055()
    myIMU.operatingMode()
    
    while True:
        #print(myIMU.calibration())
        print(myIMU.getData())