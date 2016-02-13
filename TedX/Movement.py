import time
import pygame
import datetime

from robotControl import robotControl
robots = robotControl('COM4')

case1 = -1
case2 = -1
target1 = datetime.datetime.now() + datetime.timedelta(days=10)
target2 = datetime.datetime.now() + datetime.timedelta(days=10)
firstTime = True
firstTime2 = True
direction1 = 'x'
direction2 = 'x'
straightTime1 = 1
straightTime2 = 1


#straightTime amount of time spent going to forward or backwards
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

def bounce1():
    global target1, case1, firstTime
    if case1 == 0:
        if firstTime:
            print "robot 1 case 0"
            if (direction1 == 'b'):
                robots.setSpeed(0, -50, -50)
            elif (direction1 == 'f'):
                robots.setSpeed(0, 50, 50)
            target1 = datetime.datetime.now() + datetime.timedelta(seconds=straightTime1)
            firstTime = False

    elif case1 == 1:
        if firstTime:
            print "robot 1 case 1"
            robots.setSpeed(0, -50, 50)
            target1 = datetime.datetime.now() + datetime.timedelta(milliseconds=500)
            firstTime = False

    elif case1 == 2:
        if firstTime:
            print "robot 1 case 2"
            robots.setSpeed(0, 0, 0)
            target1 = datetime.datetime.now() + datetime.timedelta(milliseconds=100)
            firstTime = False

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
            target2 = datetime.datetime.now() + datetime.timedelta(milliseconds=500)
            firstTime2 = False

    elif case2 == 2:
        if firstTime2:
            print "robot 2 case 2"
            robots.setSpeed(1, 0, 0)
            target2 = datetime.datetime.now() + datetime.timedelta(milliseconds=100)
            firstTime2 = False

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

def isAutoing(robot):
    global case1, case2
    if robot == 0:
        return case1 != -1
    if robot == 1:
        return case2 != -1

def doTele(robot, left, right):
    if isAutoing(robot) == False:
        robots.setSpeed(robot, left * -100, right * -100)

def reset():
    global case1, case2, target1, target2
    robots.setSpeed(0,0,0)
    robots.setSpeed(1,0,0)
    case1 = -1
    case2 = -1

def stop(robot):
    robots.setSpeed(robot, 0, 0)

