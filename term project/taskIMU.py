'''!@file    taskIMU.py
    @brief   IMU Task: interacts with bno055 class and IMU.
    @details The class that updates the IMU data.
    @author  Alexander Dunn
    @author  Emma Jacobs
    @date    February 03, 2022
 '''
from time import ticks_us, ticks_add, ticks_diff


def taskIMUFcn(period, theta, thetaDot, myIMU):
    '''!@brief Updates the IMU data
        @param period how often taskIMU updates
        @param theta angle of platform from IMU
        @param thetaDot angular velocity from IMU
        @param myIMU IMU object created in bno055
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
            myPos = myIMU.pos
            myVelocity = myIMU.velocity
            theta.write(myPos)
            thetaDot.write(myVelocity)

            # Update Position
            if state == 0:
                myIMU.update()


            yield state

        else:
            yield None
