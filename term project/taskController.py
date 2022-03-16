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

innerLoop = closedLoop.ClosedLoop()
outerLoop = closedLoop.ClosedLoop()
innerLoop.setMax(45)
outerLoop.setMax(45)

pitchOffset = 0
rollOffset = 0

m1Offset = 0 # -x motor
m2Offset = 0 # +y motor

def taskControllerFcn(period, theta, thetaDot, innerGain, outerGain, sVar,
                      position, velocity, motor_1, motor_2, duties, refs):
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
                innerLoop.set_Kp(innerGain.read()[0])
                innerLoop.set_Kd(innerGain.read()[1])
                outerLoop.set_Kp(outerGain.read()[0]/20.0)
                outerLoop.set_Kd(outerGain.read()[1]/20.0)
                
                state = 2
                
            # Run Controller
            elif state == 2:
                # If ball is not detected, bring back to level
                if position.read()[2] is False:
                    ref = [0,0]
                    innerLoop.set_Kp(0.45*innerGain.read()[0])
                    innerLoop.set_Kd(0.45*innerGain.read()[1])
                    innerLoop.setMax(30)
                    
                else:
                    innerLoop.set_Kp(innerGain.read()[0])
                    innerLoop.set_Kd(innerGain.read()[1])
                    innerLoop.setMax(50)
                    ref = outerLoop.run(position.read()[0], position.read()[1], 
                                        velocity.read()[0], velocity.read()[1], 
                                        0, 0)
                    
                #print(ref)
                duty = innerLoop.run(theta.read()[0]-pitchOffset, theta.read()[1]-rollOffset,
                                      thetaDot.read()[0], thetaDot.read()[1], 
                                      -ref[1], ref[0])
                
                motor_1.set_duty(duty[1] + m1Offset)
                motor_2.set_duty(duty[0] + m2Offset)
                
                duties.write([motor_1.duty, motor_2.duty])
                refs.write(ref)
                
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
                
                innerGain.write([0,0])
                outerGain.write([0,0])
                
                state = 0

# -----------------------------------------------------------------------------

            yield state

        else:
            yield None