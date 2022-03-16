'''!@file    taskTouch.py
    @brief   Touch Task: interacts with touch class and the touch panel.
    @details The class that reports and records the position of anything touching the platform.
    @author  Alexander Dunn
    @author  Emma Jacobs
    @date    March 16, 2022
 '''
from time import ticks_us, ticks_add, ticks_diff


balanceFlag = False
balanceTimer = 0

def taskTouchFcn(period, position, velocity, myTouch, tVar, filterNum):
    '''!@brief updates reading off touch panel.
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

            nextTime = ticks_add(ticks_us(), period)

            # Update Position
            if state == 0:
                myData = myTouch.update(filterNum.read())
                myPos = myData[0:3]
                myVelocity = myData[3:5]
                position.write(myPos)
                velocity.write(myVelocity)
                
                if tVar.read() == 2:
                    state = 2
                
                else:
                    state = 1
                
            # Balance Timer
            if state == 1:
                global balanceFlag
                global balanceTimer
                
                # If ball begins balancing
                if balanceFlag is False:
                    if myData[2] is True:
                        # Start the timer
                        balanceTimer = ticks_us()
                        balanceFlag = True
                
                else:
                    # If ball falls off
                    if myData[2] is False:
                        # Print elapsed time
                        myTime = ticks_diff(ticks_us(), balanceTimer)/1000000.0
                        if myTime > 0.3:
                            print(f"Ball balanced for {round(myTime, 2)} seconds")
                        balanceFlag = False
                        
                state = 0
            
            # Update calibration file
            if state == 2:
                myTouch.calibrate()
                
                tVar.write(0)
                state = 0
                        

            yield state

        else:
            yield None
