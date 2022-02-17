'''!@file    taskUser.py
    @brief   Lab0x02 (updated for Lab0x03) User Task.
    @details Allows the user to input commands to view information regarding the motor.
    @author  Emma Jacobs
    @author  Alexander Dunn
    @date    February 03, 2022
'''

import pyb
from time import ticks_us, ticks_add, ticks_diff
import closedLoop

## @brief  The serial object.
# @details Allows characters to be read from user inputs without blocking code.
#
ser = pyb.USB_VCP()
bufferString = ''
testFlag = False
cFlag = False
testTimer = 0
testList = []
speedList = []

controller = closedLoop.ClosedLoop()

def getDuty(motor):
    global bufferString
    
    # if any characters have been typed
    if ser.any():
        myChar = ser.read(1).decode()
        
        # If it's a digit
        if myChar.isdigit():
            # Append it to the string
            bufferString += myChar
            
        # If it's a minus
        elif myChar == '-':
            # Is it the first character
            if len(bufferString) == 0:
                # Append it to the string
                bufferString += myChar
            
        # If it's a backspace
        elif myChar in {'\b', '\x7f', '\x08'}:
            if len(bufferString) > 0:
                bufferString = bufferString.rstrip(bufferString[-1])
             
        # Print current string
        print(bufferString)
        
        # If it's an enter
        if myChar in {'\r', '\n'}:
            myDuty = int(bufferString)
            
            if myDuty > 100:
                myDuty = 100
            elif myDuty < -100:
                myDuty = -100
                
            motor.set_duty(myDuty)
            bufferString = ''
            state = 1
            global testTimer
            testTimer = ticks_us()
            return state
        
        else:
            state = 7
            return state
        
    else:
        state = 7
        return state
    
def getGain(controller):
    global bufferString
    
    # if any characters have been typed
    if ser.any():
        myChar = ser.read(1).decode()
        
        # If it's a decimal in the first place
        if myChar == '.':
            bufferString += myChar
        
        # If it's a digit
        elif myChar.isdigit():
            # Append it to the string
            bufferString += myChar
            
        # If it's a backspace
        elif myChar in {'\b', '\x7f', '\x08'}:
            if len(bufferString) > 0:
                bufferString = bufferString.rstrip(bufferString[-1])
             
        # Print current string
        print(bufferString)
        
        # If it's an enter
        if myChar in {'\r', '\n'}:
            myKp = float(bufferString)
            print(f"My gain = {myKp}")
            controller.set_Kp(myKp)
            bufferString = ''
            print("Choose motor speed [RPM]")
            state = 13
            # global testTimer
            # testTimer = ticks_us()
            return state
        else:
            state = 12
            return state
        
    else:
        state = 12
        return state
    
def getSpeed(controller):
    global bufferString
    
    # if any characters have been typed
    if ser.any():
        myChar = ser.read(1).decode()
        
        # If it's a digit
        if myChar.isdigit():
            # Append it to the string
            bufferString += myChar
            
        # If it's a minus
        elif myChar == '-':
            # Is it the first character
            if len(bufferString) == 0:
                # Append it to the string
                bufferString += myChar
            
        # If it's a backspace
        elif myChar in {'\b', '\x7f', '\x08'}:
            if len(bufferString) > 0:
                bufferString = bufferString.rstrip(bufferString[-1])
             
        # Print current string
        print(bufferString)
        
        # If it's an enter
        if myChar in {'\r', '\n'}:
            mySpeed = int(bufferString)
            print(f"Target speed = {mySpeed}")
            controller.ref = mySpeed
            bufferString = ''
            state = 1
            # global testTimer
            # testTimer = ticks_us()
            return state
        else:
            state = 13
            return state
        
    else:
        state = 13
        return state


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
    print("|Command: v      print encoder velocity|")
    print("|Command: m      set motor 1 duty cycle|")
    print("|Command: M      set motor 2 duty cycle|")
    print("|Command: c       clear fault condition|")
    print("|Command: g        collect encoder data|")
    print("|Command: t              run speed test|")
    print("|Command: s        end collection early|")
    print("+--------------------------------------+")
    

def taskUserFcn(taskName, period, zFlag, gFlag, pVar, dVar, gTime, gArray, tArray, index, driver, motor_1, motor_2):
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
    
    global bufferString
    bufferString = ''

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
                global testFlag

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
                        
                    elif charIn in {'m', 'M'}:
                        if charIn == 'm':
                            motor = motor_1
                        else:
                            motor = motor_2
                            
                        bufferString = ''
                        state = 7
                    
                    elif charIn in {'c', 'C'}:
                        state = 8
                        
                    elif charIn in {'v', 'V'}:
                        state = 9
            
                    
                    elif charIn in {'t', 'T'}:
                        global testTimer
                        global testList
                        global speedList
                        
                        # Reset testing parameters
                        testList = []
                        speedList = []
                        #testTimer = ticks_us()
                        testFlag = True
                        
                        #state = 10
                        print("Entering test, press 's' at any time to exit.")
                        print("Select a duty cycle to begin")
                        motor = motor_1
                        state = 7
                        
                    elif charIn in {'w', 'W'}:
                        global cFlag
                        
                       
                        if cFlag is True:
                            cFlag = False
                        else:
                            cFlag = True  
                            state = 12
                            print('Choose a gain value')
                            
                    elif charIn in {'k','K'}:
                        print("Choose a new gain")
                        state = 12
                        
                    elif charIn in {'y', 'Y'}:
                        print("Choose a new motor speed [RPM]")
                        state = 13
                            
                    elif charIn in {'r', 'R'}:
                        pass
                        
                    
                    

                # If you were controlling, keep controlling
                elif cFlag is True:
                    state = 11
                    
                # If no additional data was sent, and you're running a test, keep testing
                elif testFlag is True:
                    state = 10
                
                

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
                global testFlag
                global speedList
                # If you were running a test
                if testFlag is True:
                    global testFlag
                    testFlag = False
                    print("Test concluded")
                    print("Duty Cylce [%],Speed [rpm]")
                    for duty in speedList:
                        print(f"{duty[0]},{duty[1]}")
                    
                
                # If you were collecting data
                else:
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
                
            # Set duty
            elif state == 7:
                state = getDuty(motor)

                        
            # Reset flag
            elif state == 8:
                print("reseting")
                motor.set_duty(0)
                driver.enable()
                print("Fault reset")
                state = 1
                
                
            # Print velocity
            elif state == 9:
                # Velocity = (delta [ticks] / period [s]) / CPR [ticks/rev]
                print(f"Velocity = {60*(dVar.read()/(-period/1000000))/4000}")
                state = 1
                
            
            # Run velocity test
            elif state == 10:
                global testTimer
                global testList
                global speedList
                
                # Run Test
                if ticks_diff(ticks_us(), testTimer) < 2000000:
                    velocity = 60*(dVar.read()/(-period/1000000))/4000
                    testList.append(velocity)
                    print(f"Velocity = {60*(dVar.read()/(-period/1000000))/4000}")
                    state = 1
                
                # Continue test for 2 seconds between each run
                if ticks_diff(ticks_us(), testTimer) > 2000000:
                    # Take average and reset list
                    averageSpeed = 0
                    for speed in testList:
                        averageSpeed += speed
                    averageSpeed /= len(testList)
                    testList = []
                    
                    speedList.append([motor_1.duty, averageSpeed])
                    print("Get new duty cycle")
                    motor = motor_1
                    state = 7
                  
            # Run Controller
            elif state == 11:                
                velocity = 60*(dVar.read()/(-period/1000000))/4000

                duty = controller.run(velocity)
                motor_1.set_duty(duty)

                state = 1

            # Update Controller Gain
            elif state == 12:
                state = getGain(controller)
                
            # Update COntroller Speed
            elif state == 13:
                state = getSpeed(controller)


            yield state

        else:
            yield None

