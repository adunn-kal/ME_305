'''!@file    taskUser.py
    @brief   User Task: shows the user the help menu and interfaces with features.
    @details Allows the user to input commands to view information regarding the motor.
    @author  Emma Jacobs
    @author  Alexander Dunn
    @date    February 03, 2022
'''

import pyb
import array
import os
from time import ticks_us, ticks_add, ticks_diff

## @brief  The serial object.
# @details Allows characters to be read from user inputs without blocking code.
#
ser = pyb.USB_VCP()

## @brief  The string from characters in the serial buffer.
bufferString = ''

## @brief  Indicates if platform is using control (if it is attempting to balance).
cFlag = False

## @brief  Indicates if data is being measured.
gFlag = False

## @brief  Global variable placeholder for a gain (Kp and Kd in it)
myGain = [0, 0]

## @brief  Global variables that are placeholders for inner loop Kp and Kd.
#  @details Writing this to the shared variables.
myInnerGain = [0, 0]

## @brief  Global variables that are placeholders for outer loop Kp and Kd.
#  @details Writing this to the shared variables.
myOuterGain = [0, 0]

## @brief number of measurements being used to filter.
myFilter = 4

## @brief  Time stamps stored for recorded data
timeArray = array.array('f', 100*[0])

## @brief  Angles in x direction stored for recorded data
thetaXArray = array.array('f', 100*[0])

## @brief  Angles in y direction stored for recorded data
thetaYArray = array.array('f', 100*[0])

## @brief  Angular velocity in x direction stored for recorded data
thetaDotXArray = array.array('f', 100*[0])

## @brief  Angular velocity in y direction stored for recorded data
thetaDotYArray = array.array('f', 100*[0])

## @brief  Position in x direction of ball stored for recorded data
positionXArray = array.array('f', 100*[0])

## @brief  Position in y direction of ball stored for recorded data
positionYArray = array.array('f', 100*[0])

## @brief   Velocity in x direction of ball stored for recorded data
velocityXArray = array.array('f', 100*[0])

## @brief  Velocity in y direction of ball stored for recorded data
velocityYArray = array.array('f', 100*[0])

## @brief  Duty of x direction motor stored for recorded data
dutyXArray = array.array('f', 100*[0])

## @brief  Duty of y direction motor stored for recorded data
dutyYArray = array.array('f', 100*[0])

## @brief  Reference position in x direction of ball stored for recorded data
refXArray = array.array('f', 100*[0])

## @brief  Reference position in y direction of ball stored for recorded data
refYArray = array.array('f', 100*[0])

# ---------------------------------Functions-----------------------------------
    
def getInnerKp():
    '''!@brief prompts the user for the inner Kp value and retrieves it.
        @return next state that the task needs to go back to.
    '''
    global bufferString
    global myInnerGain
    
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
            myInnerGain[0] = float(bufferString)
            bufferString = ''
            print(f"Kp set to {myInnerGain[0]}")
            
            # Set Kd
            print("Choose a Kd value (0 - 3)")
            state = 6 

            return state
        
        else:
            state = 5
            return state
        
    else:
        state = 5
        return state
    
def getInnerKd():
    '''!@brief prompts the user for the inner Kd value and retrieves it.
        @return next state that the task needs to go back to.
    '''
    global bufferString
    global myInnerGain
    
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
            myInnerGain[1] = float(bufferString)/250.0
            bufferString = ''
            print(f"Kd set to {myInnerGain[1]*250}")
                 
            state = 1
                
            return state
        
        else:
            state = 6
            return state
        
    else:
        state = 6
        return state
    

def getOuterKp():
    '''!@brief prompts the user for the outer Kp value and retrieves it.
        @return next state that the task needs to go back to.
    '''
    global bufferString
    global myOuterGain
    
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
            myOuterGain[0] = float(bufferString)
            bufferString = ''
            print(f"Kp set to {myOuterGain[0]}")
            
            # Set Kd
            print("Choose a Kd value (0 - 3)")
            state = 16 

            return state
        
        else:
            state = 15
            return state
        
    else:
        state = 15
        return state
    
def getOuterKd():
    '''!@brief prompts the user for the outer Kd value and retrieves it.
        @return next state that the task needs to go back to.
    '''
    global bufferString
    global myOuterGain
    
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
            myOuterGain[1] = float(bufferString)/250.0
            bufferString = ''
            print(f"Kd set to {myOuterGain[1]*250}")
                 
            state = 1
                
            return state
        
        else:
            state = 16
            return state
        
    else:
        state = 16
        return state


def getFilter():
    '''!@brief Updates how touch readings are averaged (between 1-7).
    '''
    global bufferString
    global myFilter
    
    # if any characters have been typed
    if ser.any():
        myChar = ser.read(1).decode()
        
        # If it's a digit
        if myChar.isdigit():
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
            myFilter = int(bufferString)
            bufferString = ''
            
            if (myFilter > 0) and (myFilter < 8):
                print(f"Now averaging {myFilter} touch readings")
                state = 1
                
            else:
                print("Invalid number, please choose a number between 1 and 7")
                state = 17
                
            return state
        
        else:
            state = 17
            return state
        
    else:
        state = 17
        return state


def printHelp():
    '''!@brief Prints a useful help message.

        @details Prints a series of command options with descriptions for the user.

        @return None.
    '''
    print("+-----------------------------------------+")
    print("|              ME 305 LAB 0x04            |")
    print("+-----------------------------------------+")
    print("|Command: h           display help message|")
    print("|Command: p             print euler angles|")
    print("|Command: P            print ball position|")
    print("|Command: v       print angular velocities|")
    print("|Command: V            print ball velocity|")
    print("|Command: k          display current gains|")
    print("|Command: i         choose new inner gains|")
    print("|Command: o         choose new outer gains|")
    print("|Command: w         enable/disable control|")
    print("|Command: t        recalibrate touch panel|")
    print("|Command: f        # of readings to filter|")
    print("|Command: g                   Collect Data|")
    print("|Command: s                         E stop|")
    print("+-----------------------------------------+")
    

def taskUserFcn(period, theta, thetaDot, position, velocity, innerGain,
                outerGain, sVar, tVar, duties, refs, filterNum):
    '''! The function to run the user task.

        @details Uses a timer to switch between different states depending on user input.
                 Works in conjunction with the encoder task.


        @param period The period in uS of the task.

        @param theta The angle of the platform.

        @param thetaDot The angular velocity of the platform.

        @param position The position of the ball.

        @param velocity The velocity of the ball.

        @param innerGain The gains for the inner control loop.
        
        @param outerGain The gains for the out control loop.
        
        @param sVar The shared variable that tells task controller which state to go.
        
        @param tVar The shared variable that tells task touch which state.
        
        @param duties Shared variable for task control for duty cycles.
        
        @param refs The shared reference position variable.
        
        @param filterNum The number of measurements used to filter the data.

        @return None.
    '''
    ## @brief  The next time the task should run.
    # @details In uS.
    #
    nextTime = ticks_add(ticks_us(), period)
    
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

# ---------------------------------State One-----------------------------------

            # Await Command
            elif state == 1:
                global testFlag

                if ser.any():
                    ## @brief  The character typed by the user.
                    # @details Read in a 'first in, first out' manner.
                    #
                    charIn = ser.read(1).decode()
                    print(f"You typed {charIn}")

                    # Print Help Message
                    if charIn in {'h', 'H'}:
                        state = 0
                    
                    # Print Euler Angles
                    elif charIn == 'p':
                        state = 2
                        
                    # Print Ball Position
                    elif charIn == 'P':
                        state = 10
                        
                    # Print Angular Velocities
                    elif charIn == 'v':
                        state = 3
                        
                    # Print Ball Velocity
                    elif charIn == 'V':
                        state = 11

                    # Enable Closed Loop Control
                    elif charIn in {'w', 'W'}:
                        global cFlag
                        global myInnerGain
                        global myOuterGain
                        
                        # Update gains
                        myInnerKp = innerGain.read()[0]
                        
                        if cFlag is True:
                            print("Control Disabled")
                            sVar.write(3)
                            cFlag = False
                        else:
                            print("Control Enabled")
                            sVar.write(0)
                            cFlag = True  
                            
                        # Only ask to set Kp if you haven't yet
                        if myInnerKp == 0:
                            myInnerGain = [8, 2.0/250.0]
                            myOuterGain = [3.1, 1.5/(250.0)]
                            innerGain.write(myInnerGain)
                            outerGain.write(myOuterGain)
                            state = 1

                    # Update Inner Gains
                    elif charIn in {'i', 'I'}:
                        state = 5
                        print('Update Inner Loop Gains')
                        print('Choose a Kp value (1 - 5)')
                        
                    # Update Outer Gains
                    elif charIn in {'o', 'O'}:
                        state = 15
                        print('Update Outer Loop Gains')
                        print('Choose a Kp value (1 - 5)')
                    
                    # E Stop
                    elif charIn in {'s', 'S'}:
                        state = 7
                        
                    # Touch Calibration
                    elif charIn in {'t', 'T'}:
                        state = 8
                        
                    # Get Data
                    elif charIn in {'g', 'G'}:
                        global gFlag, gTimer
                        
                        # Start Timer
                        gTimer = ticks_us()
                        lastTime = ticks_diff(gTimer, 100000)
                        gFlag = True
                        gIndex = 0
                        
            
                        state = 9
                        
                    # Display Gains
                    elif charIn in {'k', 'K'}:
                        state = 13
                        
                    # Change Touch Filtering
                    elif charIn in {'f', 'F'}:
                        print("Choose how many touch readings to average (1-7)")
                        state = 17
                        
                    
# -------------------------------No Character----------------------------------                  

                # If you were controlling
                elif cFlag is True:
                    state = 4
                
                # If you were measuring, keep measuring
                elif gFlag is True:
                    state = 9
                    

# ---------------------------------Sub States----------------------------------

            # Print Euler Angles
            elif state == 2:
                print(f"Euler Angles = {theta.read()}")
                state = 1
                
            # Print Ball Position
            elif state == 10:
                print(f"Ball Position = {position.read()}")
                state = 1
                
            # Print Angular Velocities
            elif state == 3:
                print(f"Angular Velocity = {thetaDot.read()}")
                state = 1
                
            # Print Ball Velocity
            elif state == 11:
                print(f"Ball Velocity = {velocity.read()}")
                state = 1
                
            # Display Current Gains
            elif state == 13:
                print(f"Outer Loop Gains: Kp = {outerGain.read()[0]}, Kd = {outerGain.read()[1]*250}")
                print(f"Inner Loop Gains: Kp = {innerGain.read()[0]}, Kd = {innerGain.read()[1]*250}")
                
                state = 1

            # Run Controller
            elif state == 4:
                global myInnerGain
                global myOuterGain

                innerGain.write(myInnerGain)
                outerGain.write(myOuterGain)
                
                if gFlag is True:
                    state = 9
                
                else:
                    state = 1

            # Update Inner Gains
            elif state == 5:
                state = getInnerKp()
                
            # Update Inner Kd
            elif state == 6:
                state = getInnerKd()
                
            # Update Outer Gains
            elif state == 15:
                state = getOuterKp()
                
            # Update Outer Kd
            elif state == 16:
                state = getOuterKd()

            # Calibrate Touch Panel
            elif state == 8:
                tVar.write(2)
                state = 1
            
            # Collect Data
            elif state == 9:
                # Measure for 10 seconds max
                timer = ticks_diff(ticks_us(), gTimer)
                
                # If timer has reached 10 seconds
                if timer > 10*1000000:
                    print("Done Measuring")
                    gIndex = 0
                    
                    # Go to E Stop state
                    state = 7
                    
                # Update all of your arrays 10 times per second
                elif ticks_diff(ticks_us(), lastTime) > 100000:
                    global timeArray, thetaXArray, thetaYArray, thetaDotXArray
                    global thetaDotYArray, positionXArray, positionYArray
                    global velocityXArray, velocityYArray, dutyXArray
                    global dutyYArray, refXArray, refYArray
                    
                    timeArray[gIndex] = timer/1000000.0
                    thetaXArray[gIndex] = theta.read()[0]
                    thetaYArray[gIndex] = theta.read()[1]
                    thetaDotXArray[gIndex] = thetaDot.read()[0]
                    thetaDotYArray[gIndex] = thetaDot.read()[0]
                    positionXArray[gIndex] = position.read()[0]
                    positionYArray[gIndex] = position.read()[1]
                    velocityXArray[gIndex] = velocity.read()[0]
                    velocityYArray[gIndex] = velocity.read()[0]
                    dutyXArray[gIndex] = duties.read()[1] # +Y motor
                    dutyYArray[gIndex] = duties.read()[0] # -X motor
                    refXArray[gIndex] = refs.read()[0]
                    refYArray[gIndex] = refs.read()[1]
                    
                    gIndex += 1
                    lastTime = ticks_us()
                    print(timer/1000000.0)
                    
                    state = 1
                    
                else:
                    state = 1
                    
            # Change Touch Filter
            elif state == 17:
                global myFilter
                state = getFilter()
                filterNum.write(myFilter)
            
            # E Stop
            elif state == 7:
                print("Stopping Everything")
                sVar.write(4)
                
                # Quit controlling
                cFlag = False
                
                # If you were taking data, write it
                if gFlag is True:
                    global timeArray, thetaXArray, thetaYArray, thetaDotXArray
                    global thetaDotYArray, positionXArray, positionYArray
                    global velocityXArray, velocityYArray, dutyXArray
                    global dutyYArray, refXArray, refYArray
                    
                    gFlag = False
                    
                    # Print all the arrays
                    if 'data.txt' in os.listdir():
                        os.remove('data.txt')
                        
                    with open("data.txt", 'w') as file:
                        myLine = "Time [s], thetaX [deg], thetaY [deg], thetaDotX [deg/s], thetaDotY [deg/s], X [mm], Y [mm], Vx [mm/s], Vy [mm/s], DutyX [%], DutyY [%], RefX [deg], RefY [deg]\n"
                        file.write(myLine)
                        print(myLine)
                        
                        for i in range(0, 100):
                            if timeArray[i] > 0:
                                myLine = f"{timeArray[i]}, "
                                myLine += f"{thetaXArray[i]}, "
                                myLine += f"{thetaYArray[i]}, "
                                myLine += f"{thetaDotXArray[i]}, "
                                myLine += f"{thetaDotYArray[i]}, "
                                myLine += f"{positionXArray[i]}, "
                                myLine += f"{positionYArray[i]}, "
                                myLine += f"{velocityXArray[i]}, "
                                myLine += f"{velocityYArray[i]}, "
                                myLine += f"{dutyXArray[i]}, "
                                myLine += f"{dutyYArray[i]}, "
                                myLine += f"{refXArray[i]}, "
                                myLine += f"{refYArray[i]}\n"
                                
                                file.write(myLine)
                                print(myLine)
                            
                    # Clear Arrays before next reading
                    timeArray = array.array('f', 100*[0])
                    thetaXArray = array.array('f', 100*[0])
                    thetaYArray = array.array('f', 100*[0])
                    thetaDotXArray = array.array('f', 100*[0])
                    thetaDotYArray = array.array('f', 100*[0])
                    positionXArray = array.array('f', 100*[0])
                    positionYArray = array.array('f', 100*[0])
                    velocityXArray = array.array('f', 100*[0])
                    velocityYArray = array.array('f', 100*[0])
                    dutyXArray = array.array('f', 100*[0])
                    dutyYArray = array.array('f', 100*[0])
                    refXArray = array.array('f', 100*[0])
                    refYArray = array.array('f', 100*[0])
                
                state = 1

# -----------------------------------------------------------------------------

            yield state

        else:
            yield None

