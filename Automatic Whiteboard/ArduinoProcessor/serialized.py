import serial
import time
import os

data = serial.Serial('/dev/cu.usbmodem14601',9600,timeout=1)
time.sleep(5) ## WAIT
mypath = os.path.dirname(__file__)
dataChar = ''
toSend = ''


if __name__ == "__main__":
    f = open(mypath+"/output.txt","r")
    

    if f.mode == 'r':
        #time.sleep(2)
        print("READY")
        with f as fileobj:
            for line in f:  
                for ch in line: 
                    x = str.encode(ch)
                    data.write(x)   
                    print(x)
                    print(data.readline())


                    
        

        