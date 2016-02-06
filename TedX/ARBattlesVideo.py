import numpy as np
import time
import math
import cv2
import pygame
import calibrate as cs
screen = pygame.display.set_mode((640, 500))

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
blue = (73, 109, 173)
white = (255, 255, 255)

# Set the height and width of the display
displaywidth = 640
displayheight = 500

blueLower = np.array([170,50,50])
blueUpper = np.array([185,255,255])
cap = cv2.VideoCapture(0);

class ARBattlesVideo:

    SQUAREBOT = 1
    TRIANGLEBOT = 2
    PENTABOT = 3

    tempFrame = 0

    def __init__(self):
        self.originX = 244
        self.originY = 233
        self.width = 149
        self.hieght = 123

    def calibrate(self):
        obj = cs.Calibrate()
        obj.calibrate()
        x,y,w,h = obj.getCoordinates()
        self.originX = x
        self.originY = y
        self.width = w
        self.hieght = h


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
                for i in range(0,len(cnts)):
                    if i < NUM_OF_ROBOTS:
                        tempXCenter = self.getCenterX(cnts[i])
                        tempYCenter = self.getCenterY(cnts[i])
                        while(tempXCenter<=0 or tempYCenter<=0):
                            cnts =self.getContours()[0:NUM_OF_BLUE]
                            tempXCenter = self.getCenterX(cnts[i])
                            tempYCenter = self.getCenterY(cnts[i])
                            #print(tempXCenter)
                        XB[self.determineShape(cnts[i])]=self.getCenterX(cnts[i])
                        YB[self.determineShape(cnts[i])]=self.getCenterY(cnts[i])
                        #print "Big stuff"
                    else:
                        tempXCenter = self.getCenterX(cnts[i])
                        while(tempXCenter<=0 or tempYCenter<=0):
                            cnts =self.getContours()[0:NUM_OF_BLUE]
                            tempXCenter = self.getCenterX(cnts[i])
                            tempYCenter = self.getCenterY(cnts[i])
                            #print(tempXCenter)
                        XS[self.determineShape(cnts[i])]=self.getCenterX(cnts[i])
                        YS[self.determineShape(cnts[i])]=self.getCenterY(cnts[i])
                        #print "Small Stuff"
                    #print  XB,XS,YB,YS
                #print("hi7")
                notFound = False
            except:
                #print"err2"
                continue
        #print(XS,YS,XB,YB)
        if(roboID == 1):
            tempXo=XS["Quadrilateral"] - (XB["Quadrilateral"]-XS["Quadrilateral"])
            tempYo=YS["Quadrilateral"] - (YB["Quadrilateral"]-YS["Quadrilateral"])
            #print(tempXo,tempYo)
            return self.cvt021(XS["Quadrilateral"], YS["Quadrilateral"]), self.cvt021(XB["Quadrilateral"], YB["Quadrilateral"])
        if(roboID == 2):
            return self.cvt021(XS["Triangle"], YS["Triangle"]), self.cvt021(XB["Triangle"], YB["Triangle"])
        return XB,XS,YB,YS
    def determineShape(self,cnts):
        SHAPES=["0","1","2","Triangle", "Quadrilateral", "5", "6"]
        approx = cv2.approxPolyDP(cnts, 0.07*cv2.arcLength(cnts,True),True)
        numsides = len(approx)
        #print(numsides)
        return SHAPES[numsides]
    def getCenterX(self,cnt):
        M=cv2.moments(cnt)
        if(M['m00']!=0):
             cx=int(M['m10']/M['m00'])
        else:
             cx = 0
        return float(cx)
    def getCenterY(self,cnt):
        M=cv2.moments(cnt)
        if(M['m00']!=0):
            cy=int(M['m01']/M['m00'])
        else:
            cy = 0
        return float(cy)
    def getContours(self):
        (grabbed, frame) = cap.read()
        tempFrame = frame
        #cv2.imshow("frame", frame)
        #cv2.waitKey(0)
        #cv2.imshow("hi", frame)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #HSV color scale captures a wider range of the color "blue"
        #print("hi1")
        blue = cv2.inRange(hsv, blueLower, blueUpper)
        #print("hi2")
        blue = cv2.medianBlur(blue, 3) # get rid of salt and pepper
        #print("hi3")
        (cnts, _) = cv2.findContours(blue.copy(), cv2.RETR_EXTERNAL,
    	    cv2.CHAIN_APPROX_SIMPLE)
        #print("hi4")
        #print(cnts)
        #cv2.imshow("Tracking",blue)
        return sorted(cnts,key = cv2.contourArea, reverse = True)

    def cvt021(self, xRaw, yRaw):
        return float((xRaw-self.originX)/self.width), float((yRaw-self.originY)/self.hieght)

    def closeTo(self, value1, value2, range):
        if(math.fabs(value2-value1) <= range):
            return True
        return False

#TEST
#object = ARBattlesVideo()
#object.calibrate()
#print(object.originX, object.originY, object.width, object.hieght)
#time.sleep(10)
#time.sleep(5)
#print(object.robotLocation(1))
#print(object.robotLocation(2))
#print(object.robotLocation(1))
#cv2.imshow("Frame", object.tempFrame)
cv2.waitKey(0)

