import serial
ser = serial.Serial('/dev/cu.usbmodemFA121', 9600)

while True:
    ser.write(b'1')
