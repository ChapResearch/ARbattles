import serial
import time


"""
c = serial.Serial(3, 115200)

while True:
    signal = c.read()
    print signal
    print "running"
    time.sleep(2)
    c.flushOutput()
"""

"""
serial.Serial() = ser

ser.baudrate = 115200
ser.port = 'COM4'
ser.open()
ser.write(b'hello')
"""


ser = serial.Serial(3,115200, timeout=1) # open serial port


print(ser.name)# check which port was really used
ser.write("+")
ser.write("SF,1")     # write a string

timeout_start = time.time()

# timeout variable can be omitted, if you use specific value in the while condition
timeout = 30   # [seconds]

print "pre while"
while time.time() < timeout_start + timeout:
    print "pre-read"
    print ser.read()
    print "hello"
    #time.sleep(5)
    
ser.close()             # close port
print "closed"
exit

