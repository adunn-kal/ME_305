'''!@file    taskTouch.py
    @brief    Task.
    @details The class that reports and records the position of the motor.
    @author  Alexander Dunn
    @author  Emma Jacobs
    @date    February 03, 2022
 '''
from time import ticks_us, ticks_add, ticks_diff


def taskTouchFcn(period, position, velocity, myTouch):
    '''! 
    '''
    ## @brief  The next time the task should run.
    #  @details In uS.
    #
    nextTime = ticks_add(ticks_us(), period)

    ## @brief The state that the program is in.
    #  @details Begins at 0 and moves to new states based on the values of 
    #   shared variables
    #
    state = 0

    while True:
        ## @brief  The current time.
        #  @details In uS.
        #
        currentTime = ticks_us()

        if ticks_diff(currentTime, nextTime) >= 0:

            nextTime = ticks_add(ticks_us(), period)

            # Update Position
            if state == 0:
                myData = myTouch.update()
                myPos = myData[0:3]
                myVelocity = myData[3:5]
                position.write(myPos)
                velocity.write(myVelocity)
                #print(velocity.read())

            yield state

        else:
            yield None
