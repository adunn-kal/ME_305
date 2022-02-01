'''!@file    taskEncoder.py
    @brief   Lab0x02 Encoder Task.
    @details The class that reports and records the position of the motor.
    @author  Alexander Dunn
    @author  Emma Jacobs
    @date    February 03, 2022
 '''
import pyb
import encoder
from time import ticks_us, ticks_add, ticks_diff
import array

pinB6 = pyb.Pin(pyb.Pin.cpu.B6)
pinB7 = pyb.Pin(pyb.Pin.cpu.B7)


def taskEncoderFcn(taskName, period, zFlag, gFlag, pVar, dVar, gTime, gArray, tArray):

    nextTime = ticks_add(ticks_us(), period)
    global pinB6
    global pinB7
    myEncoder = encoder.Encoder(pinB6, pinB7, 4)
    state = 0

    while True:

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
                if gFlag:
                    # Get old arrays
                    posArray = gArray.read()
                    timeArray = tArray.read()
                    
                    # Add new info to arrays
                    posArray[int(gTime.read())] = myEncoder.position()
                    timeArray[int(gTime.read())] = gTime.read()
                    
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
