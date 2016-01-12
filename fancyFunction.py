import numpy as np
import time
import math
import cv2

# GrayScale bounds
#blueLower = np.array([100, 67, 0], dtype = "uint8")
#blueUpper = np.array([255, 128, 50], dtype = "uint8")

#HSV bounds
blueLower = np.array([105,50,50])
blueUpper = np.array([125,255,255])
SHAPES=["0","1","2","Triangle", "Quadrilateral", "5", "6"]


class RoboShape:
    def __init__(self, contour):
        self.contour=contour
        self.type = self.determineShape(contour)
        M=cv2.moments(self.contour)
        if(M['m00']!=0):
            self.cx=int(M['m10']/M['m00'])
            self.cy=int(M['m01']/M['m00'])
        else:
            self.cx = 0
            self.cy = 0
        return

    def determineShape(self,cnts):
        self.approx = cv2.approxPolyDP(cnts, 0.1*cv2.arcLength(cnts,True),True)
        self.numsides = len(self.approx)
        return SHAPES[self.numsides]

    def getType(self):
        return type
def determineShape(cnts):
        approx = cv2.approxPolyDP(cnts, 0.1*cv2.arcLength(cnts,True),True)
        numsides = len(approx)
        return SHAPES[numsides]
# get USB webcam input

def getPosition(frame):
    print "Running"
    robotTfront = 0,0
    robotSfront = 0,0
	# grab the current frame

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #HSV color scale captures a wider range of the color "blue"
    # determine which pixels fall within the blue boundaries
    # and then blur the binary image

    blue = cv2.inRange(hsv, blueLower, blueUpper)
    blue = cv2.medianBlur(blue, 3) # get rid of salt and pepper
    #blue = cv2.GaussianBlur(blue, (3, 3), 0) # works better

    (cnts, _) = cv2.findContours(blue.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    NUM_OF_BLUE=4
    NUM_OF_ROBOTS=NUM_OF_BLUE/2
    XB={}
    XS={}
    YB={}
    YS={}
    # check to see if any contours were found
    if len(cnts) >= NUM_OF_BLUE:
        # sort the contours and find the largest one -- we
        # will assume this contour correspondes to the robots
        cnt1 = sorted(cnts, key = cv2.contourArea, reverse = True)
        cnt1 = cnt1[0:NUM_OF_BLUE]
        # compute the (rotated) bounding box around then
        # contour and then draw it
        roboShapes=[RoboShape(contour) for contour in cnt1]
        for i in range(0,len(roboShapes)):
            thisType=roboShapes[i].type
            if i < NUM_OF_ROBOTS:
                XB[thisType]=roboShapes[i].cx
                YB[thisType]=roboShapes[i].cy

            else:
                XS[thisType]=roboShapes[i].cx
                YS[thisType]=roboShapes[i].cy
        robotTfront = XS[SHAPES[3]] - (XB[SHAPES[3]]-XS[SHAPES[3]]),YS[SHAPES[3]] - (YB[SHAPES[3]]-YS[SHAPES[3]])
        robotSfront = XS[SHAPES[4]] - (XB[SHAPES[4]]-XS[SHAPES[4]]),YS[SHAPES[4]] - (YB[SHAPES[4]]-YS[SHAPES[4]])
        """for i in range(3,len(SHAPES)):
            if SHAPES[i] in XS and SHAPES[i] in XB:
                cv2.circle(frame, ((XS[SHAPES[i]] - (XB[SHAPES[i]]-XS[SHAPES[i]]),YS[SHAPES[i]] - (YB[SHAPES[i]]-YS[SHAPES[i]]))), 2, (0,255,0),3)
                if(SHAPES[i] == "Triangle"):
                    robotTfront = ((XS[SHAPES[i]] - (XB[SHAPES[i]]-XS[SHAPES[i]]),YS[SHAPES[i]] - (YB[SHAPES[i]]-YS[SHAPES[i]])))
                if(SHAPES[i] == "Quadrilateral"):
                    robotSfront = ((XS[SHAPES[i]] - (XB[SHAPES[i]]-XS[SHAPES[i]]),YS[SHAPES[i]] - (YB[SHAPES[i]]-YS[SHAPES[i]])))
                print robotSfront
                print "Ended"
                return robotSfront,robotTfront"""
        return robotSfront, robotTfront

# cleanup the camera and close any open windows
cap = cv2.VideoCapture(1)
(grabbed, frame) = cap.read()
print getPosition(frame)