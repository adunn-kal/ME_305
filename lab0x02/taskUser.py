import pyb
from time import ticks_us, ticks_add, ticks_diff

ser = pyb.USB_VCP()

def printHelp():
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
    
def taskUserFcn(taskName, period, zFlag, gFlag, pVar, dVar, gList, gTime):
    
    nextTime = ticks_add(ticks_us(), period)
    timerStart = 0
    
    state = 0
    
    while True:
        
        currentTime = ticks_us()
        
        if ticks_diff(currentTime,nextTime) >= 0:
            
            nextTime = ticks_add(ticks_us(), period)
            
            # Innit
            if state == 0:
                printHelp()
                state = 1
            
            # Await Command
            elif state == 1:
                
                if ser.any():
                    charIn = ser.read(1).decode()
                    print(f"You typed {charIn}")
                    
                    if charIn in {'z', 'Z'}:
                        state = 2
                        #print('moving to state 2')
                    
                    elif charIn in {'h', 'H'}:
                        state = 0
                    
                    elif charIn in {'p', 'P'}:
                        state = 3
                        #print('moving to state 3')
                    
                    elif charIn in {'d', 'D'}:
                        state = 4
                        #print('moving to state 4')
                    
                    elif charIn in {'g', 'G'}:
                        state = 5
                        #print('moving to state 5')
                        
                    elif charIn in {'s', 'S'}:
                        state = 6
                        #print('moving to state 6')
                        
                # If you've collected data for 30 seconds
                if gFlag.read():
                    gTime.write(ticks_diff(ticks_us(),timerStart))
                    
                    if state != 6:
                        print(f"{gTime.read()},{pVar.read()}")
                    
                    # print(f"gTime = {gTime.read()}")
                    if gTime.read() > 30*1000000:
                        state = 6
                        #print('moving to state 6')
            
            # Zero Encoder
            elif state == 2:
                state = 1
                zFlag.write(True)
                #print("zFlag is True, moving back to s1")
            
            # Print Position
            elif state == 3:
                #print("In s3")
                print(f"Position = {pVar.read()}")
                state = 1
            
            # Print Delta
            elif state == 4:
                #print("In s4")
                print(f"Delta = {dVar.read()}")
                state = 1
            
            # Collect Data
            elif state == 5:
                # If not already recording data
                if not gFlag.read():
                    timerStart = ticks_us()
                    
                gFlag.write(True)
                state = 1
                #print("Moving to state 1")
                
            # End collection
            elif state == 6:
                """
                # Print full list with comma sep
                myList = gList.read()
                # print(f"myList = {myList}")
                for reading in range(len(myList)):
                    if isinstance(myList[reading][0], int):
                        print(f"{myList[reading][0]},{myList[reading][1]}")
                
                # Reset list and unflag gFlag
                gList.write([])
                """
                gFlag.write(False)
                state = 1
            
            yield state
            
        else:
            yield None
        

    

        
        