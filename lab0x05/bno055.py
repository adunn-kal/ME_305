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
import os


class BNO055:
    
    def __init__(self, PERIOD):
        self.imu = pyb.I2C(1, pyb.I2C.CONTROLLER)
        self.period = PERIOD
        
        # Config mode
        self.imu.mem_write(0b0000, 40, 0x3D)
        time.sleep_ms(20)
        
        # Sets up initial position and differences
        self.pos = [0, 0, 0]
        self.dif = [0, 0, 0]
        self.lastCount = 0
        self.dataList = []
        self.velocity = [0, 0, 0]
        
    def operatingMode(self, MODE):
        if MODE == "IMU":
            address = 0b1000
        if MODE == "CAL":
            address = 0b1100
        # IMU fusion mode
        self.imu.mem_write(address, 40, 0x3D)
        
    def reportCalibration(self):
        calStat = self.imu.mem_read(1, 40, 0x35)[0]
        magStat = calStat & 0b00000011
        accStat = (calStat & 0b00001100) >> 2
        gyrStat = (calStat & 0b00110000) >> 4
        sysStat = (calStat & 0b11000000) >> 6
        
        return magStat, accStat, gyrStat, sysStat
    
    def writeCalibration(self):
        # Switch mode to calibration
        self.operatingMode("CAL")
        
        # Calibrate mag
        print("Move slowly in a figure 8 pattern")
        while self.reportCalibration()[0] != 3:
            pass
        
        # Calibrate acc
        print("Move between 6 different positions")
        print("Move slowly between each and let rest a few seconds at each")
        print("Make sure one of these positions is flat")
        while self.reportCalibration()[1] != 3:
            pass
        
        # Calibrate gyr
        print("Just leave it alone for a few seconds")
        while self.reportCalibration()[2] != 3:
            pass
            
        print("Fully calibrated")
        
        # Get offset and write to file
        data = list(self.imu.mem_read(22, 40, 0x55))
        print(data)
        print(len(data))
        
        myLine = ""
        for offset in data:
            number = str(hex(offset))
            myLine += number
            myLine += ", "
        
        myLine = myLine[0:-2]
        print(myLine)
            
        file = open("IMU_cal_coeffs.txt", 'w')
        file.write(myLine)
            
        
    def readCalibration(self):
        os.remove('IMU_cal_coeffs.txt')
        file = open("IMU_cal_coeffs.txt", 'r')
        data = file.read()
        print(f"Data: {data}")
        data = data.split(', ')

        print(f"Data: {data}")

        for i in range(0, len(data)):
            data[i] = int(data[i], 16)
            self.imu.mem_write(0x55 + i, 40, data[i])
            
        print("Device Calibrated")
            
    
    def checkCalibration(self):
        # Check if calibration file has been created
        if 'IMU_cal_coeffs.txt' in os.listdir():
            file = open("IMU_cal_coeffs.txt", 'r')
            data = file.read()
            if len(data) < 22:
                os.remove('IMU_cal_coeffs.txt')
                print("No calibration file found")
                self.writeCalibration()
            
            else:
                print("Calibration file found")
                #os.remove('IMU_cal_coeffs.txt')
                self.readCalibration()
        
        # If no calibration file is present, tell user to move around until it
        # finishes calibrating
        else:
            print("No calibration file found")
            self.writeCalibration()
    
        
    def update(self):
        # Get data for each direction
        data = self.imu.mem_read(6, 40, 0x1A)
        heading, roll, pitch = struct.unpack('<hhh', data)
        
        # Roll (rotation about X)
        roll /= 16
        
        # Pitch (rotation about Y)
        pitch /= 16
        
        # Heading (rotation about Z)
        heading /= 16
        
        self.dif[0] = roll - self.pos[0]
        self.dif[1] = pitch - self.pos[1]
        self.dif[2] = heading - self.pos[2]
        self.pos = [roll, pitch, heading]
        
    
    def position(self):
        return self.pos
    
    def difference(self):
        return self.dif
        
    
    def angularVelocity(self):
        self.velocity[0] = 2*3.14159*(self.dif[0] / (-self.period/1000000)/4000)
        self.velocity[1] = 2*3.14159*(self.dif[1] / (-self.period/1000000)/4000)
        self.velocity[2] = 2*3.14159*(self.dif[2] / (-self.period/1000000)/4000)
        
        return self.velocity
        
if __name__ == "__main__":
    myIMU = BNO055(10000)
    myIMU.checkCalibration()
    myIMU.operatingMode('IMU')
    
    '''
    while True:
        #print(myIMU.reportCalibration())
        myIMU.update()
        print(myIMU.angularVelocity())
        time.sleep_us(10000)
    '''