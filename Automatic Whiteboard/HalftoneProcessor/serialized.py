import serial
import time
import os
path = os.path.dirname(__file__)
data = serial.Serial('/dev/cu.usbmodem14301',9600)

begin = False
ready = False # Only send when arduino is ready
lastMessage = ""

def sendArd(toSend):
    data.write(str.encode(str(toSend)+"+"))
    print("PYTHON -> ARDUINO:", toSend)
    data.flush()

if __name__ == "__main__":
    f = open(path+"/output.txt","r") # Open the output and start streaming it
    r = f.readlines()

    time.sleep(1)
    xx = 0
    while data.readable():
        response = data.readline()

        ### Send / Receive handling
        try:
            d = bytes.decode(response).strip()
            if d[0] == ";": # ; as first character means a debug message from the Arduino is coming
                d = d[1:] # return the message from the Arduino without the ; delimiter
                print("ARDUINO -> PYTHON: [DEBUG]",d)
            else:
                lastMessage = d
                print("ARDUINO -> PYTHON:",lastMessage)
            if not begin:
                if d == "BEGIN":
                    begin = True
                else:
                    print("-------ERROR WAITING FOR BEGIN") 
            else:
                if lastMessage == "WAIT":
                    ready = False
                elif lastMessage == "READY":
                    ready = True
            data.flush()
            lastMessage = ""
        except:
            if response != b'\n' and response != b'\r\n': ## Should only happen if python is faster than the arduino and sends empty 
                print("------- Could not decode response from Arduino:\"",response,"\"") 
            
        ###
        if begin:
            if ready:
                if xx < len(r) -1:
                    draw = r[xx].split(",")
                    drawX = draw[0]
                    drawY = draw[1]
                    drawS = draw[2].strip()
                    print("Drawing a",drawS,"sized dot at",drawX,drawY)
                    sendArd(str(draw))
                    ready = False
                    xx += 1
                else:
                    print("-------FINISHED")
                    time.sleep(100)
            else:
                #print("----- Waiting for Arduino to complete current pass")
                time.sleep(0.1)

                




        

        
