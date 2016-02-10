#
# robotControl
#
#   This module implements the control of the ARBattles robots.
#   This routine supports up to four robots currently.
#   Robots are referred to by number, starting with zero (0) for
#   the first robot, up to MAXROBOTS-1 for the last robot.
#

from rn4020 import rn4020

class robotControl:

    MAXROBOTS = 4

    TRANSMITMAX = 255
    TRANSMITMIN = 0

    #
    # robots are controlled through servos - and the servoSettings is the
    # object that stores those settings.  Servos are set to a particular
    # speed from -100 to 100.
    #

    class servoSettings:

        SERVOMAX = 100
        SERVOMIN = -100

        def __init__(self,left=0,right=0):
            self.set(left,right)

        def set(self,left,right):
            self.left = int(left)
            self.left = max(left,robotControl.servoSettings.SERVOMIN)
            self.left = min(left,robotControl.servoSettings.SERVOMAX)
            self.right = int(right)
            self.right = max(right,robotControl.servoSettings.SERVOMIN)
            self.right = min(right,robotControl.servoSettings.SERVOMAX)

        def get(self):
            return((self.left,self.right))

    #
    # __init__() - CONSTRUCTOR - must be passed the port to which the Base Station
    #              is plugged in.  Something like "COM10" for windows or "/dev/ttyUSB0"
    #              for linux.
    #
    def __init__(self,port):
        self.baseStation = rn4020(port)
        self.settings = []
        self.initRobots()

    # 
    # initRobots() - init all robots to the default settings
    #
    def initRobots(self):
        for i in range(0,robotControl.MAXROBOTS):
            self.settings.append(robotControl.servoSettings())

    #
    # setStop() - set stopped condition for the given robot.
    #             Same as setting speed to zero.
    #
    def setStop(self,robot):
        return self.setSpeed(robot,0,0)

    #
    # setSpeed() - set the speed for the given robot.  Automatically
    #              starts the trasmission of that speed to the robot
    #
    def setSpeed(self,robot,left,right):
        if robot >= 0 and robot < robotControl.MAXROBOTS:
            self.settings[robot].left = int(left)
            self.settings[robot].right = int(right)
            self.transmit()
            return True
        return False

    #
    # mapForTransmission() - given a particular servo setting, return a
    #                        two character string reprsenting that number
    #                        in the appropriate domain.
    #
    def mapForTransmission(self,servoSetting):
        value = self.remap(servoSetting, 
                           robotControl.servoSettings.SERVOMIN,robotControl.servoSettings.SERVOMAX,
                           robotControl.TRANSMITMIN,robotControl.TRANSMITMAX)
        return self.byteToHex(value)

    #
    # byteToHex() - given an int, map the lower 8 bits (0 to 255) to a two-character
    #               hex string, ready to be transmitted.  No checking is done to ensure
    #               that it is between 0 and 255 - if it is bigger, more characters come
    #
    #
    def byteToHex(self,value):
        return '{:02X}'.format(value)

    #
    # remap() - remaps a value from one range of numbers to another
    #
    def remap(self,value,oldmin,oldmax,newmin,newmax):
        return  int((float(value - oldmin) / (oldmax - oldmin)) * (newmax - newmin) + newmin)

    #
    # transmit() - transmit the current settings to the robot(s)
    #
    def transmit(self):
        outString = ""
        for i in range(0,robotControl.MAXROBOTS):
            left = self.mapForTransmission(self.settings[i].left)
            right = self.mapForTransmission(self.settings[i].right)
            outString += left + right

        # at this point we have a string ready to be transmitted through the base station

        self.baseStation.broadcast(outString)


