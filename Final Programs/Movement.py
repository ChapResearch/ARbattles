import time
import pygame
import datetime
import Line_Functions
import math

from robotControl import robotControl
robots = robotControl('COM4')

#
#   Movement Class to move the robot(s) autonomously and by joystick.
#       Only module that connects to the base station serial port.
#

case1 = -1
case2 = -1
target1 = datetime.datetime.now() + datetime.timedelta(days=100)
target2 = datetime.datetime.now() + datetime.timedelta(days=100)

#Only send the command to move if it's the first time through the loop
firstTime = True
firstTime2 = True

#Either 'f' or 'b' for forward and backward movement
direction1 = 'x'
direction2 = 'x'

#straightTime amount of time spent going to forward or backwards, optional parameter
straightTime1 = 0.5
straightTime2 = 0.5

#
# startBounce() - Given the robot, direction and optional amount of time moving straight,
#                   start the respective bounce method for boundaries or collisions.
#

def startBounce(robot, direc, sTime = 1):
    global case1, case2, direction1, direction2, straightTime1, straightTime2
    if robot == 0:
        #print "Start Bounce 1"
        case1 = 0
        direction1 = direc
        straightTime1 = sTime
        bounce1()

    elif robot == 1:
        #print "Start Bounce 2"
        case2 = 0
        direction2 = direc
        straightTime2 = sTime
        bounce2()


#
# bounce1() - Used to "bounce" off walls and other robots, preventing collisions.
#               This is robot 1, the triangle robot.
#

def bounce1():
    global target1, case1, firstTime
    if case1 == 0:
        if firstTime:
            if (direction1 == 'b'):
                robots.setSpeed(0, -50, -50)
            elif (direction1 == 'f'):
                robots.setSpeed(0, 50, 50)
            target1 = datetime.datetime.now() + datetime.timedelta(seconds=straightTime1)
            print "robot 1 case 0"
            firstTime = False

    elif case1 == 1:
        if firstTime:
            robots.setSpeed(0, -50, 50)
            target1 = datetime.datetime.now() + datetime.timedelta(milliseconds=300)
            print "robot 1 case 1"
            firstTime = False

    elif case1 == 2:
        if firstTime:
            robots.setSpeed(0, 0, 0)
            target1 = datetime.datetime.now() + datetime.timedelta(milliseconds=100)
            print "robot 1 case 2"
            firstTime = False


#
# bounce2() - Used to "bounce" off walls and other robots, preventing collisions.
#               This is robot 2, the square robot.
#
def bounce2():
    global target2, case2, firstTime2
    if case2 == 0:
        if firstTime2:
            print "robot 2 case 0"
            if (direction2 == 'b'):
                robots.setSpeed(1, -50, -50)
            elif (direction2 == 'f'):
                robots.setSpeed(1, 50, 50)

            target2 = datetime.datetime.now() + datetime.timedelta(seconds=straightTime2)
            firstTime2 = False

    elif case2 == 1:
        if firstTime2:
            print "robot 2 case 1"
            robots.setSpeed(1, -50, 50)
            target2 = datetime.datetime.now() + datetime.timedelta(milliseconds=300)
            firstTime2 = False

    elif case2 == 2:
        if firstTime2:
            print "robot 2 case 2"
            robots.setSpeed(1, 0, 0)
            target2 = datetime.datetime.now() + datetime.timedelta(milliseconds=100)
            firstTime2 = False


#
# doAuto() - Keeps track of how long autonomous functions have been running for
#               each robot and adds to the case as it goes.
#

def doAuto():
    global case1, case2, firstTime, firstTime2
    if datetime.datetime.now() > target1:
        #print "case ", case1
        firstTime = True
        if case1 < 2 and case1 > -1:
            case1 += 1
            bounce1()
        else:
            case1 = -1
    if datetime.datetime.now() > target2:
        #print "case (2) :", case2
        firstTime2 = True
        if case2 < 2 and case2 > -1:
            case2 += 1
            bounce2()
        else:
            case2 = -1


#
# isAutoing() - Returns true if the robot is currently moving autonomously
#

def isAutoing(robot, optional = 0):
    global case1, case2
    if robot == 0:
        return case1 != -1
    if robot == 1:
        return case2 != -1

#
# doTele() - Given the robot number left speed and right speed from the joystick, move the robot.
#

def doTele(robot, left, right):
    if isAutoing(robot) == False:
        robots.setSpeed(robot, left * -100, right * -100)


#
# reset() - At the end of the game, stops both robots and resets the cases to their default value.
#

def reset():
    global case1, case2, target1, target2
    robots.setSpeed(0,0,0)
    robots.setSpeed(1,0,0)
    case1 = -1
    case2 = -1


#
# stop() - Stop the robot passed to the method
#

def stop(robot):
    setSpeed(robot, 0, 0)


def setSpeed(robot, left, right):
    robots.setSpeed(robot, left, right)


def moveRobotTo(robot, currentPos, currentRotation, screenwidth, screenheight, buffer):
    if currentPos[0] > screenwidth - buffer*2:
        setSpeed(robot, -50, -50)
        print "bottom wall"

    elif currentPos[1] > screenheight - buffer*2:
        setSpeed(robot, -50, -50)
        print "right wall"

    elif currentPos[0] < 0 + buffer*2:
        setSpeed(robot, 50, 50)
        print "left wall"

    elif currentPos[1] < 0 + buffer*2:
        setSpeed(robot, 50, 50)
        print "top wall"

    else:
        print "THE ELSE"

def endGameSequence(centerPos1, centerPos2, rotationRobot1, rotationRobot2, distance, buffer, speed, displaywidth, displayheight):
    distance1 = distance
    distance2 = distance
    futureForward1 = [centerPos1[0] + speed * math.cos(rotationRobot1), centerPos1[1] + speed * math.sin(rotationRobot1)]
    futureBackward1 = [centerPos1[0] - speed * math.cos(rotationRobot1), centerPos1[1] - speed * math.sin(rotationRobot1)]

    if not Line_Functions.isHittingAnyBoundary(futureForward1, distance, 30, displaywidth, displayheight) and not Line_Functions.isIntersecting(futureBackward1, centerPos2, distance, distance, 20):
        print "Move Forward 1"
        startBounce(0, 'f', 0.5)

    elif not Line_Functions.isHittingAnyBoundary(futureBackward1, distance1, 30, displaywidth, displayheight)and not Line_Functions.isIntersecting(futureBackward1, centerPos2, distance1, distance2, 20):
        print "Move Backward 1"
        startBounce(0, 'b', 0.5)
    else:
        print "Stop 2"
        stop(1)

    futureForward2 = [centerPos2[0] + speed * math.cos(rotationRobot2), centerPos2[1] + speed * math.sin(rotationRobot2)]
    futureBackward2 = [centerPos2[0] - speed * math.cos(rotationRobot2), centerPos2[1] - speed * math.sin(rotationRobot2)]

    if not Line_Functions.isHittingAnyBoundary(futureForward2, distance2, 30, displaywidth, displayheight)and not Line_Functions.isIntersecting(centerPos1, futureForward2, distance1, distance2, 20):
        print "Move Forward 2"
        startBounce(1, 'f', 0.5)
    elif not Line_Functions.isHittingAnyBoundary(futureBackward2, distance2, 30, displaywidth, displayheight)and not Line_Functions.isIntersecting(centerPos1, futureBackward2, distance1, distance2, 20):
        print "Move Backward 2"
        startBounce(1, 'b', 0.5)
    else:
        print "Stop 2"
        stop(1)
