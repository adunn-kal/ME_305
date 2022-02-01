'''!@file    taskUser.py
    @brief   Lab0x02 User Task.
    @details Allows the user to input commands to view information regarding the motor.
    @author  Emma Jacobs
    @author  Alexander Dunn
    @date    February 03, 2022
'''

import pyb
from time import ticks_us, ticks_add, ticks_diff
import array

## @brief  The serial object.
# @details Allows characters to be read from user inputs without blocking code.
#
ser = pyb.USB_VCP()


def printHelp():
    '''! Prints a useful help message.

        @details Prints a series of command options with descriptions for the user.

        @return None.
    '''
    print("+--------------------------------------+")
    print("|            ME 305 LAB 0x02           |")
    print("+--------------------------------------+")
    print("|Command: h        display help message|")
    print("|Command: z               reset encoder|")
    print("|Command: p      print encoder position|")
    print("|Command: d         print encoder delta|")
    print("|Command: g        collect encoder data|")
    print("|Command: s        end collection early|")
    print("+--------------------------------------+")


def taskUserFcn(taskName, period, zFlag, gFlag, pVar, dVar, gTime, gArray, tArray, index):
    '''! The function to run the user task.

        @details Uses a timer to switch between different states depending on user input.
                 Works in conjunction with the encoder task.

        @param taskName The name of the task.

        @param period The period in uS of the task.

        @param zFlag The shared variable associated with the zero command.

        @param gFlag The shared variable associated with the data collection command.

        @param pVar The shared variable holding position information.

        @param dVar The shared variable holding encoder delta information.

        @param gTime The shared variable holding data collection timing information.
        
        @param gArray The shared variable holding collected data.
        
        @param gTime The shared variable holding collected times.

        @return None.
    '''
    ## @brief  The next time the task should run.
    # @details In uS.
    #
    nextTime = ticks_add(ticks_us(), period)
    
    ## @brief  The time that the data collection began.
    # @details In uS.
    #
    timerStart = 0

    ## @brief  The current state.
    #
    state = 0

    while True:
        ## @brief  The current time.
        # @details In uS.
        #
        currentTime = ticks_us()

        if ticks_diff(currentTime, nextTime) >= 0:

            nextTime = ticks_add(ticks_us(), period)

            # Innit
            if state == 0:
                printHelp()
                state = 1

            # Await Command
            elif state == 1:

                if ser.any():
                    ## @brief  The character typed by the user.
                    # @details Read in a 'first in, first out' manner.
                    #
                    charIn = ser.read(1).decode()
                    print(f"You typed {charIn}")

                    if charIn in {'z', 'Z'}:
                        state = 2

                    elif charIn in {'h', 'H'}:
                        state = 0

                    elif charIn in {'p', 'P'}:
                        state = 3

                    elif charIn in {'d', 'D'}:
                        state = 4

                    elif charIn in {'g', 'G'}:
                        state = 5

                    elif charIn in {'s', 'S'}:
                        state = 6

                # If you're collecting data, print it
                if gFlag.read():
                    # Update gTime in mS
                    gTime.write(ticks_diff(ticks_us(), timerStart)/1000.0)

                    """
                    # Print time and position values
                    if state != 6:
                        print(f"{gTime.read()},{pVar.read()}")
                    """

                    # If the timer has expired
                    if gTime.read() > 30*1000:
                        state = 6

            # Zero Encoder
            elif state == 2:
                state = 1
                zFlag.write(True)

            # Print Position
            elif state == 3:
                print(f"Position = {pVar.read()}")
                state = 1

            # Print Delta
            elif state == 4:
                print(f"Delta = {dVar.read()}")
                state = 1

            # Collect Data
            elif state == 5:
                # If not already recording data
                if not gFlag.read():
                    # Create start timer in mS
                    timerStart = ticks_us()

                gFlag.write(True)
                state = 1

            # End collection
            elif state == 6:
                # Reset index
                index.write(0)
                
                # Print full list with comma sep
                posArray = gArray.read()
                timeArray = tArray.read()

                for (time, pos) in zip(timeArray, posArray):
                    # If it's a number greater than zero
                    if isinstance(pos, int):
                        if time > 0.01:
                            print(f"{time},{pos}")
                            
                # Reset arrays and unflag gFlag
                i = 0
                while i < 3001:
                    posArray[i] = 0
                    timeArray[i] = 0
                    i += 1
                
                gArray.write(posArray)
                tArray.write(timeArray)
                
                gFlag.write(False)
                state = 1

            yield state

        else:
            yield None
