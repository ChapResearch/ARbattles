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
#                   and finds the degrees distence from east
#
def rotationOfLine(point1, point2):
    x = point1[0] - point2[0]
    y = point1[1] - point2[1]
    return math.atan2(y,x)


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
