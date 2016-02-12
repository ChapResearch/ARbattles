import numpy as np
import time
import math
import cv2
import Queue

# GrayScale bounds
#blueLower = np.array([100, 67, 0], dtype = "uint8")
#blueUpper = np.array([255, 128, 50], dtype = "uint8")

#HSV bounds
blueLower = np.array([110,50,50])
blueUpper = np.array([120,255,255])
SHAPES=["0","1","2","Triangle", "Quadrilateral", "5", "6"]
class bullet:
    def __init__(self, xO, yO, cx, cy):
        self.x = xO
        self.y = yO
        self.deltaX = cx-self.x
        self.deltaY = cy-self.y
        self.gone = False

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
    def generateOrien(self,cx1,cx2,cy1,cy2):
        self.xO = cx2 - (cx1-cx2)
        self.yO = cy2 - (cy1-cy2)
    def getType(self):
        return type

def determineShape(cnts):
        approx = cv2.approxPolyDP(cnts, 0.1*cv2.arcLength(cnts,True),True)
        numsides = len(approx)
        return SHAPES[numsides]

def checkBullets(bullets1, bullets2, heigth, width): # does editing bullets 1 change TBullets?
    for i in range(0,bullets1.size()):
        if(bullets1[i].x<0 or bullets1[i].x > width or bullets1[i].y <0 or bullets1[i].y>heigth):
            bullets1[i].gone = True
    for i in range(0,bullets2.size()):
        if(bullets2[i].x<0 or bullets2[i].x > width or bullets2[i].y <0 or bullets2[i].y>heigth):
            bullets2[i].gone = True

def drawBullets(bullets1, bullets2):
    for i in range(0,bullets1.size()):
        if(not bullets1[i].gone):
            cv2.circle(frame, (bullets1[i].x,bullets1[i].y), 2, (0,255,0),3)
            bullets1[i].x+=bullets1[i].deltaX/2
            bullets1[i].y+=bullets1[i].deltaY/2
        # remove the bullet, TODO change bullet lists to Lists

    for i in range(0,bullets2.size()):
        if(not bullets2[i].gone):
            cv2.circle(frame, (bullets2[i].x,bullets2[i].y), 2, (0,255,0),3)
            bullets2[i].x+=bullets2[i].deltaX/2
            bullets2[i].y+=bullets2[i].deltaY/2
        # remove the bullet,change bullet lists to Lists



cap = cv2.VideoCapture(1); # get USB webcam input

# keep looping
count = 0
start = time.time()
print "Running"
TbulletQueue = Queue.queue()
QbulletQueue = Queue.queue()
(grabbed, frame) = cap.read()
hight, width, channels = frame.shape
while True:

	# grab the current frame
    (grabbed, frame) = cap.read()
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

        for i in range(0,NUM_OF_ROBOTS):
            if(roboShapes[i].type == "Triangle"):
                roboShapes[i].generateOrien(XB["Triangle"],XS["Triangle"],YB["Triangle"], YS["Triangle"])
            else:
                roboShapes[i].generateOrien(XB["Quadrilateral"],XS["Quadrilateral"],YB["Quadrilateral"], YS["Quadrilateral"])

        if cv2.waitKey(1) & 0xFF == ord("b"):#add bullet
            for i in range(0,2):
                if(roboShapes[i].type == "Triangle"):
                    TbulletQueue.put(bullet(roboShapes[i].xO,roboShapes[i].yO,roboShapes[i].cx, roboShapes[i].cy))
        if cv2.waitKey(1) & 0xFF == ord("v"):#add bullet
            for i in range(0,2):
                if(roboShapes[i].type == "Quadrilateral"):
                    QbulletQueue.put(bullet(roboShapes[i].xO,roboShapes[i].yO,roboShapes[i].cx, roboShapes[i].cy))
        #for i in range(3,len(SHAPES)):
        #    if SHAPES[i] in XS and SHAPES[i] in XB:
        #        cv2.circle(frame, ((XS[SHAPES[i]] - (XB[SHAPES[i]]-XS[SHAPES[i]]),YS[SHAPES[i]] - (YB[SHAPES[i]]-YS[SHAPES[i]]))), 2, (0,255,0),3)

        for i in range(0, NUM_OF_BLUE):
            box = cv2.minAreaRect(cnt1[i])
            box1 = cv2.cv.BoxPoints(box)
            box2 = np.int32(box1)
            if(buffer and (QbulletQueue.size()>0 or TbulletQueue.size()>0) ):
                checkBullets(QbulletQueue, TbulletQueue, hight, width)
                drawBullets(QbulletQueue,TbulletQueue)
                buffer = False
            else:
                buffer = True
            #x,y,w,h = cv2.boundingRect(cnt1[i]) #get position of robots
            #print(box1[0][0]) positions drift ~ 1 pixel
            """cv2.drawContours(frame, [box2], -1, (0, 255, 0), 2)
            cv2.putText(frame,determineShape(cnt1[i]),(x+w/2,y+h/2), cv2.FONT_HERSHEY_COMPLEX_SMALL,1, (0,255,0))
            cv2.circle(frame, (x+w/2,y+h/2), 2, (0,255,0),3)"""


    #show the real-time frame and the binary image - comment out to reduce time
    cv2.imshow("Tracking", frame)
    cv2.imshow("Binary", blue)

    #if computer is slow, probably want to
    #comment out this line
    #time.sleep(0.025)

    count = count+ 1
    #if count >=150: #use to find true runtime
    #    break
    # if the 'q' key is pressed, stop the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

end = time.time()
secondsPerLoop = (end-start)/count
print secondsPerLoop
print 1/secondsPerLoop
print "Ended"
# cleanup the camera and close any open windows
cap.release()
cv2.destroyAllWindows()