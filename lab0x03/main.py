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

from pyb import Pin
import taskEncoder
import taskUser
import shares
import array
from motor import Motor
from drv8847 import DRV8847

## @brief    A flag for the zero input.
#  @details  True when the user types "Z".
#            False when the position has been zeroed
#
zFlag = shares.Share(False)

## @brief    A flag for the data collection input.
#  @details  True when the user types "G".
#            False when 30 seocnds have passed or the user stops collection early.
#
gFlag = shares.Share(False)

## @brief    The number of microseconds data has been recorded so far.
#  @details  Starts at zero and ticks up to 30e6 before it is reset.
#
gTime = shares.Share()

## @brief    The shared position value.
#  @details  Measured in ticks, can be positive or negative.
#
pVar = shares.Share()

## @brief    The shared difference value.
#  @details  Measured in ticks, can be positive or negative.
#            Measures difference between last position and the current position.
#
dVar = shares.Share()

## @brief    The shared position array.
#  @details  Measured in ticks, can be positive or negative.
#
#gArray = shares.Share(array.array('H', []))
gArray = shares.Share(array.array('l', 3001*[0]))

## @brief    The shared time array.
#  @details  In units of mS.
#
#tArray = shares.Share(array.array('f', []))
tArray = shares.Share(array.array('H', 3001*[0]))

index = shares.Share(0)


if __name__ == "__main__":
    # Instantiate driver object
    myDriver = DRV8847(Pin.cpu.A15, Pin.cpu.B2, 3)
    motor_1 = myDriver.makeMotor(Pin.cpu.B4, Pin.cpu.B5, 1, 2)
    motor_2 = myDriver.makeMotor(Pin.cpu.B0, Pin.cpu.B1, 3, 4)
    
    myDriver.enable()
    
    # Instantiate task objects
    
    ## @brief    The user task.
    #  @details  Includes name, period, and all neccesary shared variables.
    #
    userTask = taskUser.taskUserFcn('Task User', 10000, zFlag, gFlag, pVar, dVar, gTime, gArray, tArray, index, myDriver, motor_1, motor_2)
    
    ## @brief    The encoder task.
    #  @details  Includes name, period, and all neccesary shared variables.
    #
    encoderTask = taskEncoder.taskEncoderFcn('Task encoder', 10000, zFlag, gFlag, pVar, dVar, gTime, gArray, tArray, index)
    
    ## @brief    A list of tasks.
    #  @details  Includes all tasks in the order they should be performed.
    #
    taskList = [userTask, encoderTask]

    while True:
        try:
            for task in taskList:
                next(task)

        except KeyboardInterrupt:
            break

    print("Keybaord Interrupt, stopping")
