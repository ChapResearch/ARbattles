import numpy as np
import time
import math
import cv2

blueLower = np.array([105,50,50])
blueUpper = np.array([125,255,255])
SHAPES=["0","1","2","Triangle", "Quadrilateral", "5", "6"]
def determineShape(cnts):
        approx = cv2.approxPolyDP(cnts, 0.1*cv2.arcLength(cnts,True),True)
        numsides = len(approx)
        return SHAPES[numsides]
def getCenterX(cnt):
    M=cv2.moments(cnt)
    if(M['m00']!=0):
         cx=int(M['m10']/M['m00'])
    else:
         cx = 0
    return cx
def getCenterY(cnt):
    M=cv2.moments(cnt)
    if(M['m00']!=0):
         cy=int(M['m01']/M['m00'])
    else:
         cy = 0
    return cy
def getPosition(frame):
    #print "Running"
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #HSV color scale captures a wider range of the color "blue"
    blue = cv2.inRange(hsv, blueLower, blueUpper)
    blue = cv2.medianBlur(blue, 3) # get rid of salt and pepper
    #print "hi"
    (cnts, _) = cv2.findContours(blue.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    NUM_OF_BLUE=4
    NUM_OF_ROBOTS=NUM_OF_BLUE/2
    XB={}
    XS={}
    YB={}
    YS={}
    # check to see if any contours were found
    cv2.imshow("Tracking", frame)
    cv2.imshow("Blue", blue)
    XB["Triangle"] = 0
    XS["Triangle"] = 0
    YB["Triangle"] = 0
    YS["Triangle"] = 0
    XB["Quadrilateral"] = 0
    XS["Quadrilateral"] = 0
    YB["Quadrilateral"] = 0
    YS["Quadrilateral"] = 0
    if len(cnts) >= NUM_OF_BLUE:
        cnt1 = sorted(cnts, key = cv2.contourArea, reverse = True)
        cnt1 = cnt1[0:NUM_OF_BLUE]

        for i in range(0,len(cnt1)):
            if i < NUM_OF_ROBOTS:
                XB[determineShape(cnt1[i])]=getCenterX(cnt1[i])
                YB[determineShape(cnt1[i])]=getCenterY(cnt1[i])
                #print "Big stuff"

            else:
                XS[determineShape(cnt1[i])]=getCenterX(cnt1[i])
                YS[determineShape(cnt1[i])]=getCenterY(cnt1[i])
                #print "Small Stuff"
        #print  XB,XS,YB,YS
        return XB,XS,YB,YS
    return 0,0


