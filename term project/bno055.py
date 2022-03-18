'''!@file    BNO055.py
    @brief   IMU driver.
    @author  Emma Jacobs
    @author  Alexander Dunn
    @date    February 24, 2022
'''
import pyb
import time
import struct
import os


class BNO055:
    '''!@brief      Creates an object for the IMU.
        @details    Calibrates the IMU and returns the angular position and velocity 
                    data.
    '''
    
    def __init__(self, PERIOD):
        '''!@brief  Initializes the IMU.
            @param  PERIOD defines the period that the IMU data is read at.
        '''
        
        ## @brief establish I2C communication between the MCU and IMU.
        self.imu = pyb.I2C(1, pyb.I2C.CONTROLLER)
        
        ## @brief define the period that the IMU data is read at.
        self.period = PERIOD
        
        # Config mode
        self.imu.mem_write(0b0000, 40, 0x3D)
        time.sleep_ms(20)
        
        # Sets up initial position and differences
        ## @brief position on the touch screen.
        self.pos = [0, 0, 0]
        
        ## @brief velocity from IMU .
        self.velocity = [0, 0, 0]
        
    def operatingMode(self, MODE):
        '''!@brief  Sets the operating mode for the IMU.
            @param  MODE operating mode of the IMU.
        '''
        if MODE == "IMU":
            address = 0b1000
        if MODE == "CAL":
            address = 0b1100
        # IMU fusion mode
        self.imu.mem_write(address, 40, 0x3D)
        
    def reportCalibration(self):
        '''!@brief      Sets the operating mode for the IMU.
            @return     status of calibration.
        '''
        calStat = self.imu.mem_read(1, 40, 0x35)[0]
        magStat = calStat & 0b00000011
        accStat = (calStat & 0b00001100) >> 2
        gyrStat = (calStat & 0b00110000) >> 4
        sysStat = (calStat & 0b11000000) >> 6
        
        return magStat, accStat, gyrStat, sysStat
    
    def writeCalibration(self):
        '''!@brief Writes the calibration file for the IMU.
        '''
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

        myLine = ""
        for offset in data:
            number = str(hex(offset))
            myLine += number
            myLine += ", "
        
        myLine = myLine[0:-2]
            
        with open("IMU_cal_coeffs.txt", 'w') as file:
            file.write(myLine)
            
        
    def readCalibration(self):
        '''!@brief  Read the calibration file for the IMU.
            @details Calibrate IMU from an existing text file.
        '''
        with open("IMU_cal_coeffs.txt", 'r') as file:
            data = file.readline()
        
        # Format Data
        data = data.split(', ')

        # Write each value to the IMU
        for i in range(0, len(data)):
            data[i] = int(data[i], 16)
            self.imu.mem_write(0x55 + i, 40, data[i])
            
        print("Device Calibrated")
            
    
    def checkCalibration(self):
        '''!@brief   Check if a calibration file for the IMU has already been created.
        '''
        # Check if calibration file has been created
        if 'IMU_cal_coeffs.txt' in os.listdir():
            print("Calibration file found")
            #os.remove('IMU_cal_coeffs.txt')
            self.readCalibration()

        
        # If no calibration file is present, tell user to move around until it
        # finishes calibrating
        else:
            print("No calibration file found")
            self.writeCalibration()
    
        
    def update(self):
        '''!@brief  Updates the angular position and velocity from IMU.
        '''
        # Get data for each direction
        angles = self.imu.mem_read(6, 40, 0x1A)
        heading, roll, pitch = struct.unpack('<hhh', angles)
        
        velocities = self.imu.mem_read(6, 40, 0x14)
        Vx, Vy, Vz = struct.unpack('<hhh', velocities)
        
        # Roll (rotation about X)
        roll /= 16
        
        # Pitch (rotation about Y)
        pitch /= 16
        
        # Heading (rotation about Z)
        heading /= 16
        
        self.pos = [roll, pitch, heading]
        self.velocity = [Vx, Vy, Vz]
        
        
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