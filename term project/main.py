'''!@file    main_term.py
    @brief   Term project main file.
    @details  Runs tasks to balance ball.
    @author  Emma Jacobs
    @author  Alexander Dunn
    @date    March 18, 2022   
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

## @brief    The shared state value for controller task.
sVar = shares.Share(0)

## @brief    The shared recorded state value for touch task.
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
    
    ## @brief establishes motor object that controls rotation about y
    motor_1 = Motor(PWM_time, Pin.cpu.B4, Pin.cpu.B5, 1, 2)
    
    ## @brief establishes motor object that controls rotation about x
    motor_2 = Motor(PWM_time, Pin.cpu.B0, Pin.cpu.B1, 3, 4)
    
    # Instantiate IMU object and run calibration
    ## @brief period IMU runs at.
    imuPeriod = 5000
    
    ## @brief establishes IMU object for the bno055
    myIMU = bno055.BNO055(imuPeriod)
    myIMU.checkCalibration()
    myIMU.operatingMode('IMU')
    
    #Instatiate touch objects
    ## @brief period touch panel measures at.
    touchPeriod = 5000 # Time to run the update method once with 7 filtered measurements
    myTouch = touch.Touch(Pin.cpu.A7,Pin.cpu.A1,Pin.cpu.A6,Pin.cpu.A0,188,100, touchPeriod)
    myTouch.checkCal()
    
    
    # Instantiate task objects
    
    ## @brief    Runs the user task: takes user input and runs data collection. See userTask.py
    #  @details  Includes name, period, and all neccesary shared variables.
    userTask = taskUser.taskUserFcn(50000, theta, thetaDot, position, velocity,
                                    innerGain, outerGain, sVar, tVar, duties,
                                    refs, filterNum)
    
    ## @brief    Runs the IMU task: gets angular position and velocity data. 
    #  @details  Includes name, period, and all neccesary shared variables.
    imuTask = taskIMU.taskIMUFcn(imuPeriod, theta, thetaDot, myIMU)
    
    ## @brief    Runs controller task: implements closed loop control.
    #  @details  Inputs include angle, angular velocity, motor objects, and all neccesary 
    #            gains, duties, and reference points.
    #
    controllerTask = taskController.taskControllerFcn(5000, theta, thetaDot, innerGain,
                                                      outerGain, sVar, position, velocity, 
                                                      motor_1, motor_2, duties, refs)
    ## @brief    Runs touch task: updates linear position and velocity.
    #  @details  Includes period and all other neccesary shared variables.
    #
    touchTask = taskTouch.taskTouchFcn(touchPeriod, position, velocity,
                                       myTouch, tVar, filterNum)
        
    ## @brief    A list of all the tasks to run.
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
