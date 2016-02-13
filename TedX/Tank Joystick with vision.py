import pygame
import time
import math
import sys
import Line_Functions
import Movement
import datetime
from tanks import Tank

#Feb 9 - State of working with robots, vision and game
"""
displaywidth = 750
displayheight = 500
gameDisplay = pygame.display.set_mode([displaywidth, displayheight])
pygame.display.set_caption('Tank Game')
red3 = (202, 26, 26)

print "Draw"
gameDisplay.fill((255, 255, 255))
pygame.draw.rect(gameDisplay, red3, [0, 0, displaywidth/4, displayheight/4])
pygame.draw.rect(gameDisplay, red3,[displaywidth - 100, displayheight - 100, (displaywidth/4), (displayheight/4)])
pygame.display.update()

print "Set Target"
target = datetime.datetime.now() + datetime.timedelta(seconds=45)
while(datetime.datetime.now() < target):
    continue
"""
import ARBattlesVision as ar

vision = ar.ARBattlesVideo()
vision.calibrate()
print("calibration done")

pygame.init()

# Define Colors
white = (255, 255, 255)
WHITE = (255, 255, 255)

black = (0, 0, 0)
BLACK = (0, 0, 0)

#hit tank
red = (255, 0, 0)
red2 = (220, 0, 0)
RED = (255, 0, 0)

#player 2
BLUE = (73, 109, 173)    #player 2
blue = (73, 109, 173)
blue2 = (204, 255, 240)  #background


GREEN = (109, 157, 77)   #player 1
green = (109, 157, 77)
green2 = (0, 200, 0)


#Define Font
font = pygame.font.SysFont(None, 25)

#Sizing blocks and bullets
block_size = 10

player_sizex = 50
player_sizey = 60

bullet_sizex = 10
bullet_sizey = 10


#events to reset color after a hit
RESETEVENT = pygame.USEREVENT + 1
RESETEVENT2 = pygame.USEREVENT + 2
time = 700

distance1 = 0
distance2 = 0
x1 = 0
x2 = 0
y1 = 0
y2 = 0

color = black
color2 = black

rotationRobot1 = 0
collisionPrecedent = True

#-----Classes-----

#----Tank Circle Classes----

class Circle (pygame.sprite.Sprite):
    global x1, y1, distance1, time, RESETEVENT, rotationRobot1
    # This class represents the orientation of the GREEN tank.

    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill(white)
        #self.tank = Tank("blue")

        self.update()
        self.rect = self.image.get_rect()

    def update(self):
        pygame.draw.circle(gameDisplay, color,(x1, y1), int(60), 10)
        #self.tank.move((x1,y1), math.degrees(rotationRobot1))
        #gameDisplay.blit(self.tank.image,self.tank.pos,self.tank.pos)

    def timer(self):
        pygame.time.set_timer(RESETEVENT, time)


class Circle2 (pygame.sprite.Sprite):
    global x2, y2, distance2, time, RESETEVENT2
    # This class represents the orientation of the BLUE tank.

    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill(blue)
        self.tank = Tank("green")

        pygame.draw.circle(gameDisplay, color2,(x2, y2), int(60), 10)

        self.rect = self.image.get_rect()

    def update(self):
        pygame.draw.circle(gameDisplay, color2,(x2, y2), int(60), 10)
        #robots.setSpeed(1, 0, 0)


    def timer(self):
        pygame.time.set_timer(RESETEVENT2, time)



#-----Bullet Classes-----
class Bullet (pygame.sprite.Sprite):
    global bullet_sizex, bullet_sizey, color
    """ This class represents the missile for the Big Tank. """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Bullet, self).__init__()

        self.image = pygame.Surface([bullet_sizex, bullet_sizey])
        self.image.fill(color)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.x += (bullet_sizex * math.cos(rotationRobot1)) * 5
        self.rect.y += (bullet_sizey * math.sin(rotationRobot1)) * -5

class Bullet2 (pygame.sprite.Sprite):
    """ This class represents the missile for the Small Tank """
    global bullet_sizex, bullet_sizey, color2
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Bullet2, self).__init__()


        self.image = pygame.Surface([bullet_sizex, bullet_sizey])
        self.image.fill(color2)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.x += (bullet_sizex * math.cos(rotationRobot2))* 5
        self.rect.y += (bullet_sizey * math.sin(rotationRobot2))* -5

#--Method to draw text on screen
def message_to_screen(msg, color, xpos, ypos):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [xpos, ypos])

# --- Create the window
def closeTo(value1, value2, range):
       if(math.fabs(value2-value1) <= range):
           return True
       return False

# Set the height and width of the display
displaywidth = 750
displayheight = 500
gameDisplay = pygame.display.set_mode([displaywidth, displayheight])
pygame.display.set_caption('Tank Game')

# --- Sprite lists

# This is a list of every sprite (player and missiles)
all_sprites_list = pygame.sprite.Group()


# List of each bullet
bullet_list = pygame.sprite.Group()
bullet2_list = pygame.sprite.Group()


# Create the player tanks

#Circle 1
circle = Circle()
all_sprites_list.add(circle)

#Circle 2
circle2 = Circle2()
all_sprites_list.add(circle2)

# Loop until the game has ended
gameExit = False
gameOver = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
FPS = 20


#Init Game Variables
score = 0
score2 = 0

tankleftx = displaywidth/2+100
tanklefty = displayheight/2-10
tankleftx_c = 0
tanklefty_c = 0

tankrightx = displaywidth/2 - 120
tankrighty = displayheight/2-10
tankrightx_c = 0
tankrighty_c = 0


lastPosRobot1 = None
lastPosRobot2 = None

flickerTolerence = 0.1
flickrWidthTolerence = flickerTolerence * displaywidth
flickrHeightTolerence = flickerTolerence * displayheight

rotationRobot2 = 0
lastRotationRobot1 = None
lastRotationRobot2 = None

# Get count of joysticks
joystick_count = pygame.joystick.get_count()

# For each joystick:
joystick = pygame.joystick.Joystick(0)
joystick.init()

if joystick_count > 1:
    joystick2 = pygame.joystick.Joystick(1)
    joystick2.init()


# -------- Main Program Loop -----------
firstTime = False
while not gameExit:
    #print "hello"

    # ----- Game Over -----
    while gameOver == True:
        Movement.reset()
        bullet_list.empty()
        bullet2_list.empty()

        gameDisplay.fill(black)
        #message_to_screen("Game over, press Start to play again or Q to quit", red, displaywidth/2 - 200, displayheight/2)

        screen_text = font.render("Triangle Score " + str(score), True, blue2)
        gameDisplay.blit(screen_text, [displaywidth - 150, displayheight - 480])

        screen_text = font.render("Square Score " + str(score2), True, blue2)
        gameDisplay.blit(screen_text, [displaywidth - 710, displayheight - 480])

        if score > 9:
            screen_text = font.render("Triangle Won!", True, blue2)
            gameDisplay.blit(screen_text, [displaywidth / 2 - 50, displayheight/ 2 - 100])

        elif score2 > 9:
            screen_text = font.render("Square Won!", True, blue2)
            gameDisplay.blit(screen_text, [displaywidth / 2 - 50, displayheight/ 2 - 100])

        else:
            screen_text = font.render("It's a tie!", True, blue2)
            gameDisplay.blit(screen_text, [displaywidth / 2 - 50, displayheight/ 2 - 100])

        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                gameOver = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameExit = True
                    gameOver = False

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 10:
                    gameExit = True
                    gameOver = False

                if event.button == 9:
                    gameExit = False
                    score = 0
                    score2 = 0
                    gameOver = False


    # ----- Event Processing  -----
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            gameExit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                gameExit = True

        if event.type == pygame.JOYAXISMOTION:
            left = joystick.get_axis(1)
            right = joystick.get_axis(3)

            if abs(left) < 0.020:
                left = 0

            if abs(right) < 0.020:
                right = 0
            Movement.doTele(0, left, right)
            #robots.setSpeed(0, left * -100, right * -100)

            if joystick_count > 1:
                left2 = joystick2.get_axis(1)
                right2 = joystick2.get_axis(3)
                if abs(left2) < 0.020:
                    left2 = 0

                if abs(right2) < 0.020:
                    right2 = 0
                Movement.doTele(1, left2, right2)
                #robots.setSpeed(1, left2 * -100, right2 * -100)

        if event.type == pygame.JOYBUTTONDOWN:

            if joystick.get_button(6) or joystick.get_button(7):

                # Fire a bullet if the user hits the Blue 'X' Button
                bullet = Bullet()

                # Set the bullet so it is where the player is
                bullet.rect.x = centerRobot1[0] + rotatedPoint1[0]
                bullet.rect.y = centerRobot1[1] + rotatedPoint1[1]

                # Add the bullet to the lists
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)

            if joystick_count > 1:
                if joystick2.get_button(6) or joystick2.get_button(7):

                    # Fire a bullet if the user hits the Red 'B' Button
                    bullet2 = Bullet2()

                    # Set the bullet so it is where the player is
                    bullet2.rect.x = centerRobot2[0] + rotatedPoint2[0]
                    bullet2.rect.y = centerRobot2[1] + rotatedPoint2[1]

                    # Add the bullet to the lists
                    all_sprites_list.add(bullet2)
                    bullet2_list.add(bullet2)


        #Reset the tanks back to their original color
        if event.type == RESETEVENT:
                color = black
                circle.update()
                pygame.time.set_timer(RESETEVENT, 0)

        elif event.type == RESETEVENT2:
                color2 = black
                circle2.update()
                pygame.time.set_timer(RESETEVENT2, 0)



    # --- Game logic

    #
    # The method will be sending a tuple of the following form, where each point is expressed as(x,y) where x and y are between 0 and 1:
    #
    #    ([center-point-front-robot-1, center-point-rear-robot-1],
    #    [center-point-front-robot-2, center-point-rear-robot-2])
    #
    
    #Test Data One
    ((xS,yS),(xB,yB)) = vision.robotLocation(1) #Triangle
    ((x1S,y1S),(x1B,y1B)) = vision.robotLocation(2) #Quadrilateral

    if lastPosRobot1 == None or lastRotationRobot2==None or lastPosRobot2==None or lastRotationRobot1==None:
        while xS<=0 or yS<=0 or xB<=0 or yB<=0 or xS>=1 or yS>=1 or xB>=1 or yB>=1 or x1S<=0 or y1S<=0 or x1B<=0 or y1B<=0 or x1S>=1 or y1S>=1 or x1B>=1 or y1B>=1:
            ((xS,yS),(xB,yB)) = vision.robotLocation(1) #Triangle
            ((x1S,y1S),(x1B,y1B)) = vision.robotLocation(2) #Quadrilateral

    baddata = False

    if(xS<=0 or yS<=0 or xB<=0 or yB<=0 or xS>=1 or yS>=1 or xB>=1 or yB>=1 ):
        baddata = True
    if(x1S<=0 or y1S<=0 or x1B<=0 or y1B<=0 or x1S>=1 or y1S>=1 or x1B>=1 or y1B>=1):
        baddata = True

    #if baddata:
    #    continue
    if baddata:
        centerRobot1 = lastPosRobot1
        rotationRobot1 = lastRotationRobot1
        centerRobot2 = lastPosRobot2
        rotationRobot2 = lastRotationRobot2

    else:
        testData = [[(xS, yS), (xB, yB)], [(x1S, y1S), (x1B, y1B)]]

        #Made testData below to test out bullets
        #testData2 = [[(0.5, 0.7), (0.5,0.8)], [(0.7, 0.7), (0.7, 0.8)]]
        testData = Line_Functions.convertVisionDataToScreenCoords(testData, displaywidth, displayheight)

        #Split Test Data into two robots
        robot2 = testData[0]
        robot1 = testData[1]

        #Find centers
        centerRobot1 = Line_Functions.centerOfLine(robot1[0], robot1[1])
        centerRobot2 = Line_Functions.centerOfLine(robot2[0], robot2[1])

        #Determine the degrees the robot is facing from east
        rotationRobot1 = Line_Functions.rotationOfLine(robot1[0], robot1[1])
        rotationRobot2 = Line_Functions.rotationOfLine(robot2[0], robot2[1])

        if lastPosRobot1 is not None:
            if abs(centerRobot1[0] - lastPosRobot1[0]) > flickrWidthTolerence or abs(centerRobot1[1] - lastPosRobot1[1] > flickrHeightTolerence):
                centerRobot1 = lastPosRobot1
                rotationRobot1 = lastRotationRobot1

        if lastPosRobot2 is not None:
            if abs(centerRobot2[0] - lastPosRobot2[0]) > flickrWidthTolerence or abs(centerRobot2[1] - lastPosRobot2[1] > flickrHeightTolerence):
                centerRobot2 = lastPosRobot2
                rotationRobot2 = lastRotationRobot2

    lastPosRobot1 = centerRobot1
    lastPosRobot2 = centerRobot2
    lastRotationRobot1 = rotationRobot1
    lastRotationRobot2 = rotationRobot2

    x1 = int(centerRobot1[0]); y1 = int(centerRobot1[1]); x2 = int(centerRobot2[0]); y2 = int(centerRobot2[1])

    #Determine the distence between the two given points (Currently hardcoded)
    distance1 = 60

    distance2 = 60
    speed = 80
    rotatedPoint1 = [(math.cos(-1 * rotationRobot1) * distance1), (math.sin(-1 * rotationRobot1) * distance1)]
    rotatedPoint2 = [(math.cos(-1 * rotationRobot2) * distance2), (math.sin(-1 * rotationRobot2) * distance2)]

    Movement.doAuto()

    #Collision?
    """
     if centerRobot1[0] + distance1 > centerRobot2[0] - distance1 - 10:
         Movement.startBounce(0, 'b')
     elif centerRobot1[0] + distance1 > centerRobot2[0] - distance1 - 10:
    """

    collision = False
    #Line_Functions.isHittingBoundary(centerRobot1,distance1,30,'left', displaywidth, displayheight)
    #Check for robot collision

    if(Line_Functions.isIntersecting(centerRobot1, centerRobot2, distance1, distance2, 20)):
        #print "Touching"

        if collisionPrecedent:
            collision = True

        futureForward1 = [centerRobot1[0] + speed * math.cos(rotationRobot1), centerRobot1[1] + speed * math.sin(rotationRobot1)]
        futureBackward1 = [centerRobot1[0] - speed * math.cos(rotationRobot1), centerRobot1[1] - speed * math.sin(rotationRobot1)]
        #pygame.draw.circle(gameDisplay, green,(futureBackward1), 15, 0)

        #print "Robot 1 Boundary, backward: ", Line_Functions.isHittingAnyBoundary(futureBackward1, distance1, 30, displaywidth, displayheight)
        #print "Robot 1 Collision, backward: ", Line_Functions.isIntersecting(futureBackward1, centerRobot2, distance1, distance2, 20)
        #print "Center 1: ", centerRobot1, " ", "Future Backward 1: ", futureBackward1, " ", "Center 2: ", centerRobot2

        if not Line_Functions.isHittingAnyBoundary(futureForward1, distance1, 30, displaywidth, displayheight) and not Line_Functions.isIntersecting(futureForward1, centerRobot2, distance1, distance2, 20):
                print "Move Forward 1"
                Movement.startBounce(0, 'f', 0.5)
        elif not Line_Functions.isHittingAnyBoundary(futureBackward1, distance1, 30, displaywidth, displayheight)and not Line_Functions.isIntersecting(futureBackward1, centerRobot2, distance1, distance2, 20):
                print "Move Backward 1"
                Movement.startBounce(0, 'b', 0.5)
        else:
            print "Stop 1"
            Movement.stop(0)

        futureForward2 = [centerRobot2[0] + speed * math.cos(rotationRobot2), centerRobot2[1] + speed * math.sin(rotationRobot2)]
        futureBackward2 = [centerRobot2[0] - speed * math.cos(rotationRobot2), centerRobot2[1] - speed * math.sin(rotationRobot2)]

        #pygame.draw.circle(gameDisplay, blue,(futureBackward2), 15, 0)

        #print "Robot 2 Boundary, backward: ", Line_Functions.isHittingAnyBoundary(futureBackward2, distance2, 30, displaywidth, displayheight)
        #print "Robot 2 Collision, backward: ", Line_Functions.isIntersecting(centerRobot1, futureBackward2, distance1, distance2, 20)
        #print "Center 2: ", centerRobot2, " ", "Future Backward 2: ", futureBackward2, " ", "Center 1: ", centerRobot1

        if not Line_Functions.isHittingAnyBoundary(futureForward2, distance2, 30, displaywidth, displayheight)and not Line_Functions.isIntersecting(centerRobot1, futureForward2, distance1, distance2, 20):
            print "Move Forward 2"
            Movement.startBounce(1, 'f', 0.5)
        elif not Line_Functions.isHittingAnyBoundary(futureBackward2, distance2, 30, displaywidth, displayheight)and not Line_Functions.isIntersecting(centerRobot1, futureBackward2, distance1, distance2, 20):
            print "Move Backward 2"
            Movement.startBounce(1, 'b', 0.5)
        else:
            print "Stop 2"
            Movement.stop(1)

        if collision or collisionPrecedent:
            collision = False

    ##
    #Boundaries of each tank - Uses the Movement Class to bounce
    ##
    #if collision == False or collisionPrecedent:
    #Left Boundary
    if Line_Functions.isHittingBoundary(centerRobot1, distance1, 30, "left", displaywidth, displayheight):
        print "Robot 1 Left Wall"
        if (-1 * math.pi / 2) <= rotationRobot1 <= (math.pi / 2):
            Movement.startBounce(0, 'f')
        else:
            Movement.startBounce(0, 'b')

    #Right Boundary
    if Line_Functions.isHittingBoundary(centerRobot1, distance1, 30, "right", displaywidth, displayheight):
        print "Robot 1 Right Wall"
        if (-1 * math.pi / 2) <= rotationRobot1 <= (math.pi / 2):
            Movement.startBounce(0, 'b')
        else:
            Movement.startBounce(0, 'f')

    #Bottom Boundary
    if Line_Functions.isHittingBoundary(centerRobot1, distance1, 30, "bottom", displaywidth, displayheight):
        print "Robot 1 Bottom Wall"
        if rotationRobot1 > 0:
            #print "if 1"
            Movement.startBounce(0, 'f', 2)
        else:
            #print "else 1"
            Movement.startBounce(0, 'b', 2)

    #Top Boundary
    if Line_Functions.isHittingBoundary(centerRobot1, distance1, 30, "top", displaywidth, displayheight):
        print "Robot 1 Top Wall"

        if rotationRobot1 > 0:
            Movement.startBounce(0, 'b', 0.5)
        else:
            Movement.startBounce(0, 'f', 0.5)

    ###Robot 2###

    #Left Boundary
    if Line_Functions.isHittingBoundary(centerRobot2, distance2, 30, "left", displaywidth, displayheight):
        print "Robot 2 Left Wall"
        if (-1 * math.pi / 2) <= rotationRobot2 <= (math.pi / 2):
            Movement.startBounce(1, 'f')
        else:
            Movement.startBounce(1, 'b')

    #Right Boundary
    if Line_Functions.isHittingBoundary(centerRobot2, distance2, 30, "right", displaywidth, displayheight):
        print "Robot 2 Right Wall"
        if (-1 * math.pi / 2) <= rotationRobot2 <= (math.pi / 2):
            Movement.startBounce(1, 'b')
        else:
            Movement.startBounce(1, 'f')

    #Bottom Boundary
    if Line_Functions.isHittingBoundary(centerRobot2, distance2, 30, "bottom", displaywidth, displayheight):
        print "Robot 2 Bottom Wall"
        if rotationRobot2 > 0:
            Movement.startBounce(1, 'f', 2)

        else:
            Movement.startBounce(1, 'b', 2)

    #Top Boundary
    if Line_Functions.isHittingBoundary(centerRobot2, distance2, 30, "top", displaywidth, displayheight):
        print "Robot 2 Top Wall"
        if rotationRobot2 > 0:
            Movement.startBounce(1, 'b', 0.5)
        else:
            Movement.startBounce(1, 'f', 0.5)

#End of collision if



    # Call the update() method on all the sprites
    all_sprites_list.update()
    circle.update()

    # Calculate collisions for bullets from player 1
    for bullet in bullet_list:
        # If player 2 is hit, remove the bullet, add to the player 1 score and turn the player 2 tank Blue 2
        if centerRobot2[0] + distance2 > bullet.rect.x > centerRobot2[0] - distance2 and centerRobot2[1] + distance2 > bullet.rect.y > centerRobot2[1] - distance2:
            color2 = blue
            #Movement.startBounce(1, 'b', 0)
            circle2.timer()
            #print "Hit Triangles"
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

            if score <= 8.5 and score2 != -15:
                score+= 1

            else:
                score+=1
                gameOver = True

            # print"Score: ", score, "\n"

        # Remove the bullet if it flies up off the screen
        elif bullet.rect.x > displaywidth + 10 or bullet.rect.y > displayheight + 10 or bullet.rect.x < -5 or bullet.rect.y < -5:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)


            #Use the code below to penalize tank 1 for missing after shooting
            if score <= 8.5 and score2 != -10:
                score -= 0.5
                print ("Tank 1 missed!")




    # Calculate collisions for bullets from player 2
    for bullet2 in bullet2_list:

        # If the player 1 is hit, remove the bullet, add to the player 2 score and turn the player 1 tank Blue 2
        if centerRobot1[0] + distance1 > bullet2.rect.x > centerRobot1[0] - distance1 and centerRobot1[1] + distance1 > bullet2.rect.y > centerRobot1[1] - distance1:
            color = blue
            #Movement.startBounce(0, 'b', 0)
            circle.timer()
            #print "Hit Squares"
            bullet2_list.remove(bullet2)
            all_sprites_list.remove(bullet2)

            if score2 <= 8.5 and score != -15:
                score2 += 1

            else:
                score2 += 1
                gameOver = True

        # Remove the bullet if it flies up off the screen
        elif bullet2.rect.x > displaywidth + 10 or bullet2.rect.y > displayheight + 10 or bullet2.rect.x < -5 or bullet2.rect.y < -5:
            bullet2_list.remove(bullet2)
            all_sprites_list.remove(bullet2)


            #Use the code below to penalize tank 2 for missing after shooting
            if score2 <= 8.5 and score != -10:
                score2 -= 0.5
                print ("Tank 2 missed!")

    # --- Draw a frame

    # Clear the screen
    gameDisplay.fill(white)

    # Draw all the spites
    all_sprites_list.draw(gameDisplay)
    circle.update()
    circle2.update()
    
    #Draw Orientation Points
    pygame.draw.circle(gameDisplay, blue,( int(rotatedPoint1[0] + centerRobot1[0] + 10), int(rotatedPoint1[1]+ centerRobot1[1] + 15)), 10, 0)
    pygame.draw.circle(gameDisplay, green,( int(rotatedPoint2[0] + centerRobot2[0] + 2),  int(rotatedPoint2[1] + centerRobot2[1] + 15)), 10, 0)

    #Draw scores in the top corners
    screen_text = font.render("Triangle Score " + str(score), True, blue)
    gameDisplay.blit(screen_text, [displaywidth - 180, displayheight - 480])

    screen_text = font.render("Square Score " + str(score2), True, blue)
    gameDisplay.blit(screen_text, [displaywidth - 710, displayheight - 480])

    
    #Update the screen
    pygame.display.flip()
    
    # --- Limit to frames per second
    clock.tick(FPS)

    
pygame.quit()
sys.exit()
quit()


