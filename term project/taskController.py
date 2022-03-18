'''!@file    taskController.py
    @brief   Controller task: runs the inner and outer loop control.
    @details Implements closed loop PD control.
    @author  Alexander Dunn
    @author  Emma Jacobs
    @date    March 18, 2022
 '''
from time import ticks_us, ticks_add, ticks_diff
import closedLoop

## @brief object for inner loop control
innerLoop = closedLoop.ClosedLoop()

## @brief object for outerloop control
outerLoop = closedLoop.ClosedLoop()
innerLoop.setMax(45)
outerLoop.setMax(45)

pitchOffset = 0
rollOffset = 0

m1Offset = 0 # -x motor
m2Offset = 0 # +y motor

def taskControllerFcn(period, theta, thetaDot, innerGain, outerGain, sVar,
                      position, velocity, motor_1, motor_2, duties, refs):
    '''!@brief Calls the controller class to perform.
        @param period how often the task runs in us
        @param theta angle of the platform
        @param thetaDot angular velocity of the platform
        @param innerGain gains of the inner control loop
        @param outerGain gains of the outer control loop
        @param sVar the shared state variable
        @param position location of the ball on touch panel
        @param velocity velocity of the ball
        @param motor_1 object for the x motor
        @param motor_2 object for the y motor
        @param duties duty cycles
        @param refs reference values for the ball
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