'''!@file    main.py
    @brief   Lab0x03 main file.
    @details Create a user interface to use an encoder and return 30 seconds of 
    data from the motor.
    @author  Emma Jacobs
    @author  Alexander Dunn
    @date    February 16, 2022
    

    @author              Alexander Dunn
    @author Emma Jacobs

    @date                February 2, 2022
    
'''

from pyb import Pin, Timer
import taskIMU
import taskUser
import taskController
import shares
from motor import Motor
import bno055


## @brief    The shared position value.
#  @details  Measured in ticks, can be positive or negative.
#
pVar = shares.Share()

## @brief    The shared velocity value.
#  @details  Measured in rad/s, can be positive or negative.
#            Measures angular velocity in x, y, z.
#
vVar = shares.Share()

## @brief    The shared velocity value.
#  @details  Measured in rad/s, can be positive or negative.
#            Measures angular velocity in x, y, z.
#
KpVar = shares.Share(0)

## @brief    The shared velocity value.
#  @details  Measured in rad/s, can be positive or negative.
#            Measures angular velocity in x, y, z.
#
KdVar = shares.Share(0)

## @brief    The shared velocity value.
#  @details  Measured in rad/s, can be positive or negative.
#            Measures angular velocity in x, y, z.
#
sVar = shares.Share(0)



if __name__ == "__main__":
    # Instantiate motor objects
    PWM_time = Timer(3, freq = 20000)
    motor_1 = Motor(PWM_time, Pin.cpu.B4, Pin.cpu.B5, 1, 2)
    motor_2 = Motor(PWM_time, Pin.cpu.B0, Pin.cpu.B1, 3, 4)
    
    #nSLEEP = Pin(Pin.cpu.A15, mode=Pin.OUT_PP)
    #nSLEEP.high()
    
    # Instantiate IMU object and run calibration
    myIMU = bno055.BNO055(10000)
    myIMU.checkCalibration()
    myIMU.operatingMode('IMU')
    
    
    # Instantiate task objects
    
    ## @brief    The user task.
    #  @details  Includes name, period, and all neccesary shared variables.
    #
    userTask = taskUser.taskUserFcn(10000, pVar, vVar, KpVar, KdVar, sVar)
    
    ## @brief    The IMU task.
    #  @details  Includes name, period, and all neccesary shared variables.
    #
    imuTask = taskIMU.taskIMUFcn(10000, pVar, vVar, myIMU)
    
    ## @brief    The IMU task.
    #  @details  Includes name, period, and all neccesary shared variables.
    #
    controllerTask = taskController.taskControllerFcn(10000, pVar, vVar, KpVar,
                                                      KdVar, sVar, motor_1, motor_2)
    
    ## @brief    A list of tasks.
    #  @details  Includes all tasks in the order they should be performed.
    #
    taskList = [userTask, imuTask, controllerTask]

    while True:
        try:
            for task in taskList:
                next(task)

        except KeyboardInterrupt:
            break

    print("Keybaord Interrupt, stopping")
