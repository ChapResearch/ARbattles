import numpy as np
import time
import math
import cv2

cap = cv2.VideoCapture(0); # get USB webcam input
numPlayers = 4
# GrayScale bounds
#blueLower = np.array([100, 67, 0], dtype = "uint8")
#blueUpper = np.array([255, 128, 50], dtype = "uint8")

#HSV bounds
blueLower = np.array([160, 50, 50])
blueUpper = np.array([185, 255, 255])
def distance(point1, point2):
    sq1 = (point1[0]-point2[0])*(point1[0]-point2[0])
    sq2 = (point1[1]-point2[1])*(point1[1]-point2[1])
    return math.sqrt(sq1 + sq2)

def WithinError(a,b,c,d,e):
    if b-e < a < b+e and c-e < d <c+e and a-e< c <a+e:
        return True
    return False;

def equalSides(boxy):
    if WithinError(distance(boxy[0],boxy[1]), distance(boxy[1],boxy[2]),distance(boxy[2], boxy[3]),distance(boxy[3],boxy[0]), 15):
        return True
    return False

def determineShape(cnts):
    approx = cv2.approxPolyDP(cnts, 0.06*cv2.arcLength(cnts,True),True)
    numsides = len(approx)
    boxtemp = cv2.minAreaRect(cnt1)
    boxone = cv2.cv.BoxPoints(boxtemp)
    if numsides == 4:
       # if equalSides(boxone):
        #    return "Blue Square"
        return "Blue Quadrilateral"
    elif numsides == 3:
        return "Blue Triangle"
    #elif numsides == 5:
     #   return "Blue Pentagon"
    #elif numsides == 6:
    #    return "Blue Hexagon"
    #elif numsides == 8:
    #    return "Blue Octagon"
    #elif numsides == 7:
    #    return "Blue Septagon"
    #return "Error"


# keep looping
count = 0
start = time.time()
print "Running"
while True:

	# grab the current frame
    (grabbed, frame) = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #HSV color scale captures a wider range of the color "blue"
    # determine which pixels fall within the blue boundaries
    # and then blur the binary image
    blue = cv2.inRange(hsv, blueLower, blueUpper)
    blue = cv2.medianBlur(blue, 5) # get rid of alt and pepper
    #blue = cv2.GaussianBlur(blue, (3, 3), 0) #3,3

    (cnts, _) = cv2.findContours(blue.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)

    # check to see if any contours were found
    if len(cnts) >= numPlayers:
        # sort the contours and find the largest one -- we
        # will assume this contour correspondes to the robots
        cnt1 = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        # compute the (rotated) bounding box around then
        # contour and then draw it
        box = cv2.minAreaRect(cnt1)
        box1 = cv2.cv.BoxPoints(box)
        box2 = np.int32(box1)
        x,y,w,h = cv2.boundingRect(cnt1) #get position of robots
        #print(box1[0][0]) positions drift ~ 1 pixel

        cv2.drawContours(frame, [box2], -1, (0, 255, 0), 2)
        cv2.putText(frame,determineShape(cnt1),(x+w/2,y+h/2), cv2.FONT_HERSHEY_COMPLEX_SMALL,1, (0,255,0))
        cv2.circle(frame, (x+w/2,y+h/2), 2, (0,255,0),3)

        ############################################################### next robot
        if numPlayers >1:
            cnt1 = sorted(cnts, key = cv2.contourArea, reverse = True)[1]

            box = cv2.minAreaRect(cnt1)
            box1 = cv2.cv.BoxPoints(box)
            box2 = np.int32(box1)
            x,y,w,h = cv2.boundingRect(cnt1)

            cv2.drawContours(frame, [box2], -1, (0, 255, 0), 2)
            cv2.putText(frame,determineShape(cnt1),(x+w/2,y+h/2), cv2.FONT_HERSHEY_COMPLEX_SMALL,1, (0,255,0))
            cv2.circle(frame, (x+w/2,y+h/2), 2, (0,255,0),3)

        ###############################################################
        if numPlayers >2:
            cnt1 = sorted(cnts, key = cv2.contourArea, reverse = True)[2]

            box = cv2.minAreaRect(cnt1)
            box1 = cv2.cv.BoxPoints(box)
            box2 = np.int32(box1)
            x,y,w,h = cv2.boundingRect(cnt1)

            cv2.drawContours(frame, [box2], -1, (0, 255, 0), 2)
            cv2.putText(frame,determineShape(cnt1),(x+w/2,y+h/2), cv2.FONT_HERSHEY_COMPLEX_SMALL,1, (0,255,0))
            cv2.circle(frame, (x+w/2,y+h/2), 2, (0,255,0),3)

        ###############################################################
        if numPlayers > 3:
            cnt1 = sorted(cnts, key = cv2.contourArea, reverse = True)[3]

            box = cv2.minAreaRect(cnt1)
            box1 = cv2.cv.BoxPoints(box)
            box2 = np.int32(box1)
            x,y,w,h = cv2.boundingRect(cnt1)

            cv2.drawContours(frame, [box2], -1, (0, 255, 0), 2)
            cv2.putText(frame,determineShape(cnt1),(x+w/2,y+h/2), cv2.FONT_HERSHEY_COMPLEX_SMALL,1, (0,255,0))
            cv2.circle(frame, (x+w/2,y+h/2), 2, (0,255,0),3)
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
print (end-start)/count
print "Ended"
# cleanup the camera and close any open windows
cap.release()
cv2.destroyAllWindows()