'''!@file    taskEncoder.py
    @brief   Encoder Task.
    @details The class that reports and records the position of the motor.
    @author  Alexander Dunn
    @author  Emma Jacobs
    @date    February 03, 2022
 '''
import pyb
import encoder
from time import ticks_us, ticks_add, ticks_diff

## @brief pin B6 object
#  
pinB6 = pyb.Pin(pyb.Pin.cpu.B6)

## @brief pin B7 object
#
pinB7 = pyb.Pin(pyb.Pin.cpu.B7)


def taskEncoderFcn(taskName, period, zFlag, gFlag, pVar, dVar, gTime, gArray, tArray, index):
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
    global pinB6
    global pinB7
    
    ## @brief The encoder object being used.
    #  @details contains specific attributes and methods.
    #
    myEncoder = encoder.Encoder(pinB6, pinB7, 4)
    
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
            myPos = myEncoder.position
            myDif = myEncoder.dif
            pVar.write(myPos)
            dVar.write(myDif)

            # Update Position
            if state == 0:
                myEncoder.update()

                # If gFlag is true, add readings to arrays
                if gFlag.read():
                    # Get old arrays
                    
                    ## @brief The position array.
                    #  @details In ms. Gets the old array values and is then updated with
                    #   new ones.
                    #
                    posArray = gArray.read()
                    
                    ## @brief The time array.
                    #  @details In ms. Gets the old array values and is then updated with
                    #   new ones.
                    #
                    timeArray = tArray.read()
                    
                    # Add new info to arrays
                    if isinstance(gTime.read(), float):
                        posArray[index.read()] = myEncoder.position
                        timeArray[index.read()] = int(gTime.read())
                        
                        index.write(index.read() + 1)
                    
                    # Update shared arrays for user task
                    gArray.write(posArray)
                    tArray.write(timeArray)

                if zFlag.read():
                    state = 1

            # Zero position
            elif state == 1:
                #print(f"Encoder position was {myEncoder.position}")
                myEncoder.zero(myEncoder.position)
                #print(f"Encoder position = {myEncoder.position}")
                zFlag.write(False)
                state = 0
                #print("Moving back to s0")

            yield state

        else:
            yield None
