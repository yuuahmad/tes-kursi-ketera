import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
serialInstance = serial.Serial()

portlist = []

for port in ports:
    portlist.append(str(port))
    print(str(port))

val = input("pilih port yang ingin dibaca : ")

for x in range(0, len(portlist)):
    if portlist[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portlist[x])

serialInstance.baudrate = 9600
serialInstance.port = portVar
serialInstance.open()

while True:
    if serialInstance.in_waiting():
        paket = serialInstance.readline()
        print(paket.decode("utf-8").rstrip("\n"))

# import serial
# import time

# serialsaya = serial.Serial("COM3", 9600)
# time.sleep(2)

# # if serialsaya.in_waiting():
# paket = serialsaya.readline()
# print(paket.decode("utf-8").rstrip("\n"))
