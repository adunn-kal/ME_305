# -*- coding: utf-8 -*-
'''!@file    taskController.py
    @brief   Lab0x02 Encoder Task.
    @details The class that reports and records the position of the motor.
    @author  Alexander Dunn
    @author  Emma Jacobs
    @date    February 03, 2022
 '''
from time import ticks_us, ticks_add, ticks_diff
import closedLoop

controller = closedLoop.ClosedLoop()

def taskControllerFcn(period, pVar, vVar, KpVar, KdVar, sVar, motor_1, motor_2):
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

# -----------------------------------------------------------------------------
            
            # Check sVar
            if state == 0:
                if sVar.read():
                    state = sVar.read()
                else:
                    state = 1

            # Update Gains
            elif state == 1:
                controller.set_Kp(KpVar.read())
                controller.set_Kd(KdVar.read())
                
                state = 2
                
            # Run Controller
            elif state == 2:
                duty = controller.run(pVar.read()[0], pVar.read()[1],
                                      vVar.read()[0], vVar.read()[1])
                motor_1.set_duty(duty[1])
                motor_2.set_duty(duty[0])
                
                state = 0
            
            # Pause Controller
            elif state == 3:
                motor_1.set_duty(0)
                motor_2.set_duty(0)
                
                state = 0
            
            # E Stop
            elif state == 4:
                motor_1.set_duty(0)
                motor_2.set_duty(0)
                
                KpVar.write(0)
                KdVar.write(0)
                
                state = 0

# -----------------------------------------------------------------------------

            yield state

        else:
            yield None