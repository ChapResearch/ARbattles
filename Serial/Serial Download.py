import serial
import time

ser = serial.Serial(
    port='COM4',
    baudrate=115200,
    timeout = 10
    )

ser.close()
ser.open()


def robotaa(data):
    """Function to send robot a left motor """
    if(data!= "exit")
        ser.write(data + '\n')
    else
        ser.close()
        exit()
def robotab(data):
    """Function to send robot a right motor"""
    if(data!= "exit")
        ser.write(data + '\n')
    else
        ser.close()
        exit()
        
def robotba(data):
    """Function to send robot b left motor"""
    if(data!= "exit")
        ser.write(data + '\n')
    else
        ser.close()
        exit()
        
def robotbb(data):
    """Function to send robot b right motor """
    if(data!= "exit")
        ser.write(data + '\n')
    else
        ser.close()
        exit()
        
"""def _write_cmd(self, cmd):
    #Write a command and wait for response
    if self.debug_print: print ">" + cmd
        self._write_line(cmd);
        resp = None
    while resp == None:
      resp = self._read_line()
    if self.debug_print: print "<" + resp
    return resp
"""
