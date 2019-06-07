import serial
import time
import os

data = serial.Serial('/dev/cu.usbmodem14501',9600)
counter = 32

if __name__ == "__main__":
    while data.readable():
        counter += 1
        data.write(str.encode((str(counter))))
        print(data.readline())
        if counter == 255:
            counter = 32
        time.sleep(.4)



                    
        

        