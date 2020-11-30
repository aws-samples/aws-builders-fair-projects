import time
import serial
import csv



def probeDrum(counter, ser, delay):
        ser.write(chr(130))
        out = ''
        time.sleep(delay)
        while ser.inWaiting() > 0:
                out += ser.read(1)
        if out != '':
                print ">>" + out
        return out.replace("\n","").replace("\r","")


# configure the serial connections (the parameters differs on the device you are connecting to)

counter = 0

ser1 = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200
)
ser2 = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=115200
)
ser3 = serial.Serial(
    port='/dev/ttyUSB2',
    baudrate=115200
)
ser4 = serial.Serial(
    port='/dev/ttyUSB3',
    baudrate=115200
)
ser5 = serial.Serial(
    port='/dev/ttyUSB4',
    baudrate=115200
)

ser6 = serial.Serial(
    port='/dev/ttyUSB5',
    baudrate=115200
)

ser7 = serial.Serial(
    port='/dev/ttyUSB6',
    baudrate=115200
)

ser8 = serial.Serial(
    port='/dev/ttyUSB7',
    baudrate=115200
)

if not ser1.isOpen():
  print("Error opening port /dev/ttyUSB0")
if not ser2.isOpen():
  print("Error opening port /dev/ttyUSB1")
if not ser3.isOpen():
  print("Error opening port /dev/ttyUSB2")
if not ser4.isOpen():
  print("Error opening port /dev/ttyUSB3")
if not ser5.isOpen():
  print("Error opening port /dev/ttyUSB4")
if not ser6.isOpen():
  print("Error opening port /dev/ttyUSB5")
if not ser7.isOpen():
  print("Error opening port /dev/ttyUSB6")
if not ser8.isOpen():
  print("Error opening port /dev/ttyUSB7")



fields = ['drum','port']
filename = "drum-map.csv"
input=1
with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
	for x in range(1, 9):
		counter += 1
        	delay = 0.7
		drum = probeDrum(counter, eval("ser"+str(x)), delay)
        	print("ser"+str(x)+"is "+drum)
                csvwriter.writerow([drum,"ser"+str(x)])
        

ser1.close()
ser2.close()
ser3.close()
ser4.close()
ser5.close()
ser6.close()
ser7.close()
ser8.close()

