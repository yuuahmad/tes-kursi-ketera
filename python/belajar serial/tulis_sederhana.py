import serial
import time

ser = serial.Serial("COM3", 9600)  # open serial port
# time.sleep(2)
# print(ser.name)  # check which port was really used
ser.write(b"g")  # write a string
# time.sleep(2)
ser.close()  # close port
