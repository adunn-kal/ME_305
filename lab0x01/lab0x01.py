'''!@file lab0x01.py
    @brief Lab0x01 Assignment.
    @details Press a button to cycle through several different LED patterns.\
        Video Link: https://youtu.be/rAyXS61tPXw
    @author Emma Jacobs
    @author Alexander Dunn
    
    @mainpage

    @section sec_lab     Lab0x01
                        This is the first lab

    @section sec_url     Video URL
                        https://youtu.be/rAyXS61tPXw. 
                        
    @section sec_image FSM Transition Diagram
                        https://imgur.com/1cZLLTZ

    @author              Alexander Dunn
    @author Emma Jacobs

    @date                January 20, 2022
'''
import pyb
import time
import math

pinC13 = pyb.Pin(pyb.Pin.cpu.C13)
pinA5 = pyb.Pin(pyb.Pin.cpu.A5)
tim2 = pyb.Timer(2, freq=20000)
t2ch1 = tim2.channel(1, pyb.Timer.PWM, pin=pinA5)


def onButtonPressCallback(IRQ_src):
    '''!Sets buttonPressed flag to True when button is pressed.

        @details Updates the buttonPressed flag when the user presses the
                  button

        @param IRQ_src The interupt request.

        @return None.
    '''
    global buttonPressed
    buttonPressed = True


def SawWave(t):
    '''!Determines the appropriate brightness based on saw wave pattern.

        @details Takes a floating point number and returns it's decimal as a
                  brightness value.

        @parm t Time in seconds since pattern started.

        @return 0.0-1.0 brightness.
    '''
    return (t % 1)


def SquareWave(t):
    '''!Determines the appropriate brightness based on square wave pattern.

        @details Takes a floating point number and returns either 1 or 0
                  depending on the decimal value of the number.

        @param t Time in seconds since pattern started.

        @return On or off.
    '''
    if t % 1 < 0.5:
        return (1)
    else:
        return (0)


def SineWave(t):
    '''!Determines the appropriate brightness based on sine wave pattern

        @details Takes a floating point number and uses a sine wave to return
                  a brightness value between 0 and 1.

        @param t Time in seconds since pattern started.

        @return 0.0-1.0 brightness.
    '''
    return (math.sin((2 * 3.1415/10) * t) / 2) + 0.5


ButtonInt = pyb.ExtInt(pinC13, mode=pyb.ExtInt.IRQ_FALLING,
                       pull=pyb.Pin.PULL_NONE, callback=onButtonPressCallback)

if __name__ == '__main__':
    # Reset flag, print messages, got to state zero
    buttonPressed = False
    state = 0
    print('In State zero')
    print('Welcome to our brightness modifier. Press the blue user button to \
          cycle through LED patterns.')

    # Run continuosly
    while True:
        try:
            if state == 0:
                # Run state zero
                if buttonPressed:
                    # Reset timer, go to next pattern
                    buttonPressed = False
                    state = 1
                    print('Square wave pattern selected')
                    start = time.ticks_ms()
            elif state == 1:
                # Run state one
                brt = SquareWave((time.ticks_ms()-start)/1000)
                t2ch1.pulse_width_percent(brt*100)

                if buttonPressed:
                    buttonPressed = False
                    start = time.ticks_ms()
                    state = 2
                    print('Sine wave pattern selected')

            elif state == 2:
                # Run state two
                brt = SineWave((time.ticks_ms()-start)/1000.0)
                t2ch1.pulse_width_percent(brt*100)

                if buttonPressed:
                    buttonPressed = False
                    start = time.ticks_ms()
                    state = 3
                    print('Sawtooth wave pattern selected')

            elif state == 3:
                # Run state 3
                brt = SawWave((time.ticks_ms()-start)/1000.0)
                t2ch1.pulse_width_percent(brt*100)

                if buttonPressed:
                    buttonPressed = False
                    state = 1
                    print('Square wave pattern selected')

        # Allow keybpard interrupt to break out
        except KeyboardInterrupt:
            break

    print('Program Terminating')
