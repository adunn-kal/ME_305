'''!@file    BNO055.py
    @brief   Lab0x05 IMU driver.
    @details 
    @author  Emma Jacobs
    @author  Alexander Dunn
    @date    February 24, 2022
'''
import pyb

class BNO055:
    
    def __init__(self):
        self.imu = pyb.I2C(1, pyb.I2C.CONTROLLER)
        
    def operatingMode(self):
        self.imu.mem_write(0b1000, 40, 0x3D)
        
    def calibration(self):
        calibrationStat = self.imu.mem_read(1, 40, 0x35)
        return calibrationStat
        
        
if __name__ == "__main__":
    myIMU = BNO055()
    myIMU.operatingMode()
    
    while True:
        print(myIMU.calibration())
        