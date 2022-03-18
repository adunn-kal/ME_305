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
import taskTouch
import touch


## @brief    The shared angle value.
theta = shares.Share()

## @brief    The shared angular velocity value.
thetaDot = shares.Share()

## @brief    The shared gain values for the inner loop.
innerGain = shares.Share([0,0])

## @brief    The shared gain values for the outer loop.
outerGain = shares.Share([0,0])

## @brief    The shared state value.
sVar = shares.Share(0)

## @brief    The shared recorded time value.
tVar = shares.Share(0)

## @brief    The shared recorded velocity values.
velocity = shares.Share(0)

## @brief    The shared recorded position values.
position = shares.Share(0)

## @brief    The shared recorded duty cycles.
duties = shares.Share([0, 0])

## @brief    The shared recorded reference positions.
refs = shares.Share([0, 0])

## @brief    The number of measurements used in filtering.
filterNum = shares.Share(4)



if __name__ == "__main__":
    # Instantiate motor objects
    PWM_time = Timer(3, freq = 20000)
    motor_1 = Motor(PWM_time, Pin.cpu.B4, Pin.cpu.B5, 1, 2)
    motor_2 = Motor(PWM_time, Pin.cpu.B0, Pin.cpu.B1, 3, 4)
    
    # Instantiate IMU object and run calibration
    ## @brief period IMU runs at.
    imuPeriod = 5000
    myIMU = bno055.BNO055(imuPeriod)
    myIMU.checkCalibration()
    myIMU.operatingMode('IMU')
    
    #Instatiate touch objects
    ## @brief period touch panel measures at.
    touchPeriod = 5000 # Time to run the update method once with 7 filtered measurements
    myTouch = touch.Touch(Pin.cpu.A7,Pin.cpu.A1,Pin.cpu.A6,Pin.cpu.A0,188,100, touchPeriod)
    myTouch.checkCal()
    
    
    # Instantiate task objects
    
    ## @brief    The user task.
    #  @details  Includes name, period, and all neccesary shared variables.
    #
    userTask = taskUser.taskUserFcn(50000, theta, thetaDot, position, velocity,
                                    innerGain, outerGain, sVar, tVar, duties,
                                    refs, filterNum)
    
    ## @brief    The IMU task.
    #  @details  Includes name, period, and all neccesary shared variables.
    #
    imuTask = taskIMU.taskIMUFcn(imuPeriod, theta, thetaDot, myIMU)
    
    ## @brief    The IMU task.
    #  @details  Includes name, period, and all neccesary shared variables.
    #
    controllerTask = taskController.taskControllerFcn(5000, theta, thetaDot, innerGain,
                                                      outerGain, sVar, position, velocity, 
                                                      motor_1, motor_2, duties, refs)
    ## @brief    The IMU task.
    #  @details  Includes name, period, and all neccesary shared variables.
    #
    touchTask = taskTouch.taskTouchFcn(touchPeriod, position, velocity,
                                       myTouch, tVar, filterNum)
    
    
    ## @brief    A list of tasks.
    #  @details  Includes all tasks in the order they should be performed.
    #
    taskList = [userTask, imuTask, touchTask, controllerTask]
    

    while True:
        try:
            for task in taskList:
                next(task)

        except KeyboardInterrupt:
            break

    print("Keybaord Interrupt, stopping")
