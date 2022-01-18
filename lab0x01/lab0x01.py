#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 12:59:06 2022

@author: alexanderdunn
"""

import pyb
import time
import math

pinC13 = pyb.Pin(pyb.Pin.cpu.C13)
pinA5 = pyb.Pin(pyb.Pin.cpu.A5)
tim2 = pyb.Timer(2, freq=20000)
t2ch1 = tim2.channel(1, pyb.Timer.PWM, pin=pinA5)


def onButtonPressCallback(IRQ_src):
    """
    Sets buttonPressed flag to True when button is pressed

    Parameters
    ----------
    IRQ_src : IRQ
        Interrupt request.

    Returns
    -------
    None.

    """
    global buttonPressed
    buttonPressed = True


def SawWave(t):
    """
    Determines the appropriate brightness based on saw wave pattern

    Parameters
    ----------
    t : float
        time in seconds since pattern started.

    Returns
    -------
    float
        0-1 brightness.

    """
    return (t % 1)


def SquareWave(t):
    """
    Determines the appropriate brightness based on square wave pattern

    Parameters
    ----------
    t : float
        time in seconds since pattern started.

    Returns
    -------
    int
        On or off.

    """
    if t % 1 < 0.5:
        return (1)
    else:
        return (0)


def SineWave(t):
    """
    Determines the appropriate brightness based on sine wave pattern

    Parameters
    ----------
    t : float
        time in seconds since pattern started.

    Returns
    -------
    float
        0-1 brightness.

    """
    return (math.sin((2*3.1415/10)*t)/2) + 0.5


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
