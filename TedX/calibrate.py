import numpy as np
import math
import cv2

# oi0
# Contains calibration methods, to avoid conflicts with robotLocation
#
# interface:
#       calibrate() - assuming there are four blue corners in video frame, return the four corners
#
redLower = np.array([170,50,50])
redUpper = np.array([185,255,255])
cap = cv2.VideoCapture(1);

class Calibrate:
    def __init__(self):
        self.originX = 0.0
        self.originY = 0.0
        self.width = 0.0
        self.hieght = 0.0

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
    def getCoordinates(self):
        return self.originX, self.originY, self.width, self.hieght

    def getContours(self):
        (grabbed, frame) = cap.read()
        tempFrame = frame
        #cv2.imshow("frame", frame)
        #cv2.waitKey(0)
        #cv2.imshow("hi", frame)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #HSV color scale captures a wider range of the color "blue"
        print("hi1")
        blue = cv2.inRange(hsv, redLower, redUpper)
        print("hi2")
        blue = cv2.medianBlur(blue, 3) # get rid of salt and pepper
        print("hi3")
        (cnts, _) = cv2.findContours(blue.copy(), cv2.RETR_EXTERNAL,
    	    cv2.CHAIN_APPROX_SIMPLE)
        print("hi4")
        #print(cnts)
        #cv2.imshow("Tracking",blue)
        return sorted(cnts,key = cv2.contourArea, reverse = True)

    def closeTo(self, value1, value2, range):
        if(math.fabs(value2-value1) <= range):
            return True
        return False
