import serial
import time

"""Working one directly below"""
ser = serial.Serial(3,115200, timeout=5) # open serial port

print(ser.name)# check which port was really used
count = 1
ser.write("+")
ser.write("hello")
print "write complete"

#ser.write("SF,1")     # write a string

timeout_start = time.time()

# timeout variable can be omitted, if you use specific value in the while condition
timeout = 30
# [seconds]

print "pre while \n"
while time.time() < timeout_start + timeout:
    print "pre read"
    print ser.read(size=30)
    print "post read \n"

    ser.write(str(count) + "th round through reading")
    count+=1

ser.close()             # close port
print "closed"
exit()


"""Other test cases I am/was looking at"""

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
ser = serial.Serial()

ser.baudrate = 115200
print "baudrate set to", ser.baudrate
ser.port = 'COM4'
print "port set to", ser.port
ser.open()
print "port opened"
timeout_start = time.time()
timeout = 10   # [seconds]
count = 0
print "pre-read"
while time.time() < timeout_start + timeout:
    print "pre read loop"
    print ser.read(), "hi", count
    print "trying to read"
    count+=1
print "closing port"
ser.close()
print "port closed"
exit

"""


"""
# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM4',
    baudrate=115200,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()

print 'Enter your commands below.\r\nInsert "exit" to leave the application.'

input=1
while 1 :
    # get keyboard input
    input = raw_input(">> ")
        # Python 3 users
        # input = input(">> ")
    if input == 'exit':
        ser.close()
        exit()
    else:
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        ser.write(input + '\r\n')
        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read(1)

        if out != '':
            print ">>" + out
"""
"""
 #!/usr/bin/python

import serial, time

#initialization and open the port

#possible timeout values:

#    1. None: wait forever, block call

#    2. 0: non-blocking mode, return immediately

#    3. x, x is bigger than 0, float allowed, timeout block call
    
ser = serial.Serial()

#ser.port = "/dev/ttyUSB0"

ser.port = "COM4"

#ser.port = "/dev/ttyS2"

ser.baudrate = 115200

ser.bytesize = serial.EIGHTBITS #number of bits per bytes

ser.parity = serial.PARITY_NONE #set parity check: no parity

ser.stopbits = serial.STOPBITS_ONE #number of stop bits

#ser.timeout = None          #block read

ser.timeout = 1            #non-block read

#ser.timeout = 2              #timeout block read

ser.xonxoff = False     #disable software flow control

ser.rtscts = False     #disable hardware (RTS/CTS) flow control

ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control

ser.writeTimeout = 2     #timeout for write

try: 

    ser.open()

except Exception, e:

    print "error open serial port: " + str(e)

    exit()

if ser.isOpen():

    try:

        ser.flushInput() #flush input buffer, discarding all its contents

        ser.flushOutput()#flush output buffer, aborting current output 

                 #and discard all that is in buffer

    #write data

    ser.write("+")

    print("write data: +")

    time.sleep(0.5)  #give the serial port sometime to receive the data

    numOfLines = 0

    while True:

        response = ser.readline()

        print("read data: " + response)

        numOfLines = numOfLines + 1

        if (numOfLines >= 5):

            break

    ser.close()

    except Exception, e1:

    print "error communicating...: " + str(e1)

else:

    print "cannot open serial port "
"""
"""
import serial

port= "COM4" # or the port where you're device is connected
baudrate=115200 # or the baudrate of your device

s = serial.Serial(port, baudrate, timeout=10) # Open the port
s.write("hello!")
print "starting"
for i in range(100):
    print "pre flush input"
    s.flushInput()
    line = s.readline()
    print "pre print"
    print line
s.close()
"""
