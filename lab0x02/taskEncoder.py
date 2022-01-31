'''!@file    taskEncoder.py
    @brief   Lab0x02 Encoder Task.
    @details The class that reports and records the position of the motor.
    @author  Alexander Dunn
    @author  Emma Jacobs
    @date    January 20, 2022
 '''
import pyb
import encoder
from time import ticks_us, ticks_add, ticks_diff

pinB6 = pyb.Pin(pyb.Pin.cpu.B6)
pinB7 = pyb.Pin(pyb.Pin.cpu.B7)


def taskEncoderFcn(taskName, period, zFlag, gFlag, pVar, dVar, gTime):

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
