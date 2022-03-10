'''!@file    taskUser.py
    @brief   Lab0x02 (updated for Lab0x03) User Task.
    @details Allows the user to input commands to view information regarding the motor.
    @author  Emma Jacobs
    @author  Alexander Dunn
    @date    February 03, 2022
'''

import pyb
from time import ticks_us, ticks_add, ticks_diff

## @brief  The serial object.
# @details Allows characters to be read from user inputs without blocking code.
#
ser = pyb.USB_VCP()
bufferString = ''

cFlag = False

share = None

myGain = [0, 0]
myInnerGain = [0, 0]
myOuterGain = [0, 0]

# ---------------------------------Functions-----------------------------------
    
def getKp():
    global bufferString
    global myGain
    
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
            #myKp = float(bufferString)
            #share.write(float(bufferString))
            myGain[0] = float(bufferString)
            bufferString = ''
            
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
    
def getKd(share):
    global bufferString
    global myGain
    global cFlag
    
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
            #share.write(float(bufferString)/250.0)
            #myKd = float(bufferString)
            #myKd /= 250.0
            myGain[1] = float(bufferString)/250.0
            share.write(myGain)
            bufferString = ''
                 
            state = 1
                
            return state
        
        else:
            state = 6
            return state
        
    else:
        state = 6
        return state


def printHelp():
    '''! Prints a useful help message.

        @details Prints a series of command options with descriptions for the user.

        @return None.
    '''
    print("+-----------------------------------------+")
    print("|              ME 305 LAB 0x04            |")
    print("+-----------------------------------------+")
    print("|Command: h           display help message|")
    print("|Command: p             print euler angles|")
    print("|Command: v       print angular velocities|")
    print("|Command: i         choose new inner gains|")
    print("|Command: o         choose new outer gains|")
    print("|Command: w         enable/disable control|")
    print("|Command: s                         E stop|")
    print("+-----------------------------------------+")
    

def taskUserFcn(period, theta, thetaDot, innerGain, outerGain, sVar):
    '''! The function to run the user task.

        @details Uses a timer to switch between different states depending on user input.
                 Works in conjunction with the encoder task.


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
                    elif charIn in {'p', 'P'}:
                        state = 2
                        
                    # Print Angular Velocities
                    elif charIn in {'v', 'V'}:
                        state = 3

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
                            print("Gains set to Kp = 5, Kd = 1")
                            myInnerGain = [5, 1.0/250.0]
                            myOuterGain = [5.0, 1.0/(250.0)]
                            innerGain.write(myInnerGain)
                            outerGain.write(myOuterGain)
                            state = 1
                            
                    # Update Inner Gains
                    elif charIn in {'i', 'I'}:
                        global share
                        state = 5
                        share = innerGain
                        print('Choose a Kp value (1 - 5)')
                        
                    # Update Outer Gains
                    elif charIn in {'o', 'O'}:
                        global share
                        state = 5
                        share = outerGain
                        print('Choose a Kp value (1 - 5)')
                            
                    # E Stop
                    elif charIn in {'s', 'S'}:
                        state = 7
                        
                    
# -------------------------------No Character----------------------------------                  

                # If you were controlling, keep controlling
                elif cFlag is True:
                    state = 4

# ---------------------------------Sub States----------------------------------

            # Print Euler Angles
            elif state == 2:
                print(f"Position = {theta.read()}")
                state = 1
                
            # Print Angular Velocities
            elif state == 3:
                print(f"Velocity = {thetaDot.read()}")
                state = 1

            # Run Controller
            elif state == 4:
                global myInnerGain
                global myOuterGain
                
                #innerGain.write(myInnerGain)
                #outerGain.write(myOuterGain)

                state = 1

            # Update Inner Gains
            elif state == 5:
                state = getKp()
                
            # Update Controller Kd
            elif state == 6:
                global share
                state = getKd(share)
                
            # E Stop
            elif state == 7:
                print("Stopping Everything")
                sVar.write(4)
                
                # Quit controlling
                cFlag = False
                
                state = 1

# -----------------------------------------------------------------------------

            yield state

        else:
            yield None

