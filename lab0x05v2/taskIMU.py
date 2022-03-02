'''!@file    taskIMU.py
    @brief   Lab0x02 Encoder Task.
    @details The class that reports and records the position of the motor.
    @author  Alexander Dunn
    @author  Emma Jacobs
    @date    February 03, 2022
 '''
from time import ticks_us, ticks_add, ticks_diff


def taskIMUFcn(period, pVar, vVar, myIMU):
    '''! Calls the Encoder class to perform functions.

        @details Uses the Encoder methods and attributes to return and perform
        actions based on shared variables.
        
        @param zFlag The shared variable associated with the zero command.

        @param pVar The shared variable holding position information.

        @param dVar The shared variable holding encoder delta information.

        @return zFlag, pVar, dVar.
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
            pVar.write(myPos)
            vVar.write(myVelocity)

            # Update Position
            if state == 0:
                myIMU.update()


            yield state

        else:
            yield None
