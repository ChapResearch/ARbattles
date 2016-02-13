import math
import time

#
# centerOfLine() - This routine returns a point (consisting of (x,y))
#                   that is at the center of the two given points.
#
def centerOfLine(point1, point2):
    cx = (point1[0] + point2[0])/2
    cy = (point1[1] + point2[1])/2
    return (cx,cy)


#
# rotationOfLine() - This routine takes two points (consisting of (x,y))                       
#                   and finds the radians distance from east
#
def rotationOfLine(point1, point2):
    x = point1[0] - point2[0]
    y = point1[1] - point2[1]
    return -1 * math.atan2(y,x)


#
# convertToScreenCoords() - Given a (x,y) tuple convert it
#                           to screen coordinates and return it.
#
 
def convertToScreenCoords(point, width, height):
    return (point[0] * width, point[1] * height)


#
# convertVisionDataToScreenCoords() - Given a large tuple consisting of four tuples
#                                       return them with screen coordinates.
#
def convertVisionDataToScreenCoords(data, width, height):
    robot1 = data[0]
    robot2 = data[1]

    robot1pt1 = robot1[0]
    robot1pt2 = robot1[1]

    robot2pt1 = robot2[0]
    robot2pt2 = robot2[1]

    return [[convertToScreenCoords(robot1pt1,width, height),
             convertToScreenCoords(robot1pt2, width, height)],
            [convertToScreenCoords(robot2pt1,width, height),
             convertToScreenCoords(robot2pt2, width, height)]]

def isIntersecting(center1, center2, radius1, radius2, buffer = 0):
    distance = math.sqrt(math.pow((center1[0] - center2[0]),2) + math.pow((center1[1] - center2[1]),2))
    return distance < radius1 + radius2 + buffer

def isHittingBoundary(pos, radius, buffer, boundary, screenwidth, screenheight):

    if boundary == "left":
        return pos[0] - radius < buffer
    elif boundary == "right":
        return pos[0] + radius > screenwidth - buffer
    elif boundary == "top":
        return pos[1] - radius < buffer
    elif boundary == "bottom":
        return pos[1] + radius > screenheight - buffer

def isHittingAnyBoundary(pos, radius, buffer, screenwidth, screenheight):
    if not isHittingBoundary(pos, radius, buffer, "left", screenwidth, screenheight) and not isHittingBoundary(pos, radius, buffer, "right", screenwidth, screenheight) and not isHittingBoundary(pos, radius, buffer, "top", screenwidth, screenheight) and not isHittingBoundary(pos, radius, buffer, "bottom", screenwidth, screenheight):
        return False
    return True