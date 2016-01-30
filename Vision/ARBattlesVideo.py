import numpy as np
import time
import math
import cv2
import pygame

#screen = pygame.display.set_mode((640, 500))
# oi0
# Contains vision related methods, include recognizing the robots, determining orientation
#
# interface:
#
#       robotLocation() - returns an array of quadruples (ID, x,y,theta) where x and y are from 0 to 1
#                         where the origin is in the upper left. Theta is a measurement in degrees
#                         from East.
#       calibrate() - assuming there are four blue corners in video frame, calibrate
#

blueLower = np.array([100,50,50])
blueUpper = np.array([115,255,255])
cap = cv2.VideoCapture(0);
class ARBattlesVideo:

    SQUAREBOT = 1
    TRIANGLEBOT = 2
    PENTABOT = 3

    def __init__(self):
        self.originX = 0
        self.originY = 0
        self.width = 0
        self.hieght = 0

    def calibrate(self):
        doublecheck = 1
        firstTime = True
        while(doublecheck<=5):
            try:
                count = 0
                cnts = self.getContours()[0:2]
                x1,y1,w1,h1 = cv2.boundingRect(cnts[0])
                x2,y2,w2,h2 = cv2.boundingRect(cnts[1])
                if(firstTime or self.closeTo(x1,self.originX, 200)):
                    self.originX = x1
                    count = count +1
                if(firstTime or self.closeTo(x1,self.originY, 200)):
                    self.originY = y1
                    count = count+1
                if(firstTime or self.closeTo((x2+w2)-x1,self.width, 200)):
                    self.width = (x2+w2)-x1
                    count = count +1
                if(firstTime or self.closeTo((y2+h2)-y1,self.hieght, 200)):
                    self.hieght = (y2+h2)-y1
                    count = count +1
                if(count == 4):
                    firstTime = False
                    doublecheck = doublecheck+1
                else:
                    firstTime = True
                    doublecheck = 1
            except:
                print("err")
                continue

    def robotLocation(self, roboID):
        NUM_OF_BLUE=4
        NUM_OF_ROBOTS=NUM_OF_BLUE/2
        XB={}
        XS={}
        YB={}
        YS={}
        # check to see if any contours were found
        #cv2.imshow("Tracking", frame)
        #cv2.imshow("Blue", blue)
        XB["Triangle"] = 0
        XS["Triangle"] = 0
        YB["Triangle"] = 0
        YS["Triangle"] = 0
        XB["Quadrilateral"] = 0
        XS["Quadrilateral"] = 0
        YB["Quadrilateral"] = 0
        YS["Quadrilateral"] = 0
        notFound = True
        while(notFound):
            try:
                cnts = self.getContours()[0:NUM_OF_BLUE]
                print(len(cnts))
                for i in range(0,len(cnts)):
                    if i < NUM_OF_ROBOTS:
                        XB[self.determineShape(cnts[i])]=self.getCenterX(cnts[i])
                        YB[self.determineShape(cnts[i])]=self.getCenterY(cnts[i])
                        print "Big stuff"
                    else:
                        XS[self.determineShape(cnts[i])]=self.getCenterX(cnts[i])
                        YS[self.determineShape(cnts[i])]=self.getCenterY(cnts[i])
                        print "Small Stuff"
                    #print  XB,XS,YB,YS
                notFound = False
            except:
                print"err2"
                continue
        if(roboID == 1):
            print("hi6")
            return XS["Quadrilateral"], YS["Quadrilateral"], XS["Quadrilateral"] - (XB["Quadrilateral"]-XS["Quadrilateral"]), YS["Quadrilateral"] - (YB["Quadrilateral"]-YS["Quadrilateral"])
        if(roboID == 2):
            return XS["Triangle"], YS["Triangle"], XS["Triangle"] - (XB["Triangle"]-XS["Triangle"]), YS["Triangle"] - (YB["Triangle"]-YS["Triangle"])
        return XB,XS,YB,YS
    def determineShape(self,cnts):
        SHAPES=["0","1","2","Triangle", "Quadrilateral", "5", "6"]
        approx = cv2.approxPolyDP(cnts, 0.05*cv2.arcLength(cnts,True),True)
        numsides = len(approx)
        print(numsides)
        return SHAPES[numsides]
    def getCenterX(self,cnt):
        M=cv2.moments(cnt)
        if(M['m00']!=0):
             cx=int(M['m10']/M['m00'])
        else:
             cx = 0
        return cx
    def getCenterY(self,cnt):
        M=cv2.moments(cnt)
        if(M['m00']!=0):
            cy=int(M['m01']/M['m00'])
        else:
            cy = 0
        return cy
    def getContours(self):
        (grabbed, frame) = cap.read()
        #cv2.imshow("frame", frame)
        #cv2.waitKey(0)
        #cv2.imshow("hi", frame)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #HSV color scale captures a wider range of the color "blue"
        print("hi1")
        blue = cv2.inRange(hsv, blueLower, blueUpper)
        print("hi2")
        blue = cv2.medianBlur(blue, 5) # get rid of salt and pepper
        print("hi3")
        (cnts, _) = cv2.findContours(blue.copy(), cv2.RETR_EXTERNAL,
    	    cv2.CHAIN_APPROX_SIMPLE)
        print("hi4")
        #print(cnts)
        #cv2.imshow("Tracking",blue)
        return sorted(cnts,key = cv2.contourArea, reverse = True)

    def cvt021(self, raw):
        xRaw, yRaw = raw
        return (xRaw-self.originX)/self.width, (yRaw-self.originY)/self.hieght

    def closeTo(self, value1, value2, range):
        if(math.fabs(value2-value1) <= range):
            return True
        return False

#TEST
object = ARBattlesVideo()
object.calibrate()
print(object.originX, object.originY, object.width, object.hieght)
time.sleep(5)
print(object.robotLocation(1))

