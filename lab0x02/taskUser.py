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
    
def taskUserFcn(taskName, period, zFlag, pVar, dVar):
    
    nextTime = ticks_add(ticks_us(), period)
    
    state = 0
    
    while True:
        
        currentTime = ticks_us()
        
        if ticks_diff(currentTime,nextTime) >= 0:
            
            nextTime = ticks_add(ticks_us(), period)
            
            if state == 0:
                printHelp()
                state = 1
                
            elif state == 1:
                if ser.any():
                    charIn = ser.read(1).decode()
                    print(f"You typed {charIn}")
                    
                    if charIn in {'z', 'Z'}:
                        state = 2
                        print('moving to state 2')
                    
                    elif charIn in {'h', 'H'}:
                        state = 0
                    
                    elif charIn in {'p', 'P'}:
                        state = 3
                        print('moving to state 3')
                    
                    elif charIn in {'d', 'D'}:
                        state = 4
                        print('moving to state 4')
                    
                    elif charIn in {'g', 'G'}:
                        state = 5
                        print('moving to state 3')
                        
            elif state == 2:
                state = 1
                zFlag.write(True)
                print("zFlag is True, moving back to s1")
                
            elif state == 3:
                print("In s3")
                print(f"Position = {pVar.read()}")
                state = 1
            
            elif state == 4:
                print("In s4")
                print(f"Delta = {dVar.read()}")
                state = 1
                
            elif state == 5:
                state = 1
            
            yield state
            
        else:
            yield None
        

    

        
        