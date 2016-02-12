import time
import pygame
import datetime
"""
from robotControl import robotControl
robots = robotControl('COM4')
"""
case1 = -1
case2 = -1
target1 = datetime.datetime.now() + datetime.timedelta(days=10)
target2 = datetime.datetime.now() + datetime.timedelta(days=10)
firstTime = True
firstTime2 = True


def startBounce(robot):
    global case1, case2
    if robot == 0:
        case1 = 0
        bounce1()
        #print "Bounce 1 Started: ", case1, "\n"

    elif robot == 1:
        case2 = 0
        bounce2()
        #print "Bounce 2 Started: ", case2


def bounce1():
    global target1, case1, firstTime
    if case1 == 0:
        if firstTime:
            print "case 0: robots.setSpeed(0, -50, -50) \n"
            target1 = datetime.datetime.now() + datetime.timedelta(seconds=1)
            firstTime = False

    elif case1 == 1:
        if firstTime:
            print "case 1: robots.setSpeed(0, -50, 50) \n"
            target1 = datetime.datetime.now() + datetime.timedelta(seconds=1)
            firstTime = False

    elif case1 == 2:
        if firstTime:
            print "case 2: robots.setSpeed(0, 0, 0) \n"
            target1 = datetime.datetime.now() + datetime.timedelta(seconds=1)
            firstTime = False

def bounce2():
    global target2, case2, firstTime2
    if case2 == 0:
        if firstTime2:
            print "robot 2 case 0: robots.setSpeed(1, -50, -50)"
            target2 = datetime.datetime.now() + datetime.timedelta(seconds=1)
            firstTime2 = False
    elif case2 == 1:
        if firstTime2:
            print "robot 2 case 1: robots.setSpeed(1, -50, 50)"
            target2 = datetime.datetime.now() + datetime.timedelta(seconds=1)
            firstTime2 = False
    elif case2 == 2:
        if firstTime2:
            print "robot 2 case 2: robots.setSpeed(1, 0, 0)"
            target2 = datetime.datetime.now() + datetime.timedelta(seconds=1)
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
        print "robots.setSpeed(robot, left, right)"