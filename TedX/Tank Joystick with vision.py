import pygame
import time
import math
import sys
import Line_Functions
import ARBattlesVision as ar

#Feb 9 - State of working with robots, vision and game

vision = ar.ARBattlesVideo()
vision.calibrate()
print("calibration done")


from robotControl import robotControl

robots = robotControl('COM4')

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

color = white
color2 = white

#-----Classes-----

#----Tank Circle Classes----

class Circle (pygame.sprite.Sprite):
    global x1, y1, distance1, time, RESETEVENT
    # This class represents the orientation of the GREEN tank.

    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill(white)

        pygame.draw.circle(gameDisplay, color,(x1, y1), int(60), 0)

        self.rect = self.image.get_rect()

    def update(self):
        # Update
        #self.rect.x = x1-distance1
        #self.rect.y = y1-distance1
        pygame.draw.circle(gameDisplay, color,(x1, y1), int(60), 0)

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
        pygame.draw.circle(gameDisplay, color2,(x2, y2), int(60), 0)

        self.rect = self.image.get_rect()

    def update(self):
    #   Update
        #self.rect.x = x2-distance2
        #self.rect.y = y2-distance2
        pygame.draw.circle(gameDisplay, color2,(x2, y2), int(60), 0)

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
        self.rect.y += (bullet_sizey * math.sin(rotationRobot1)) * 5
        self.rect.x += (bullet_sizex * math.cos(rotationRobot1)) * 5

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
        self.rect.x += (bullet_sizex * math.cos(rotationRobot2))*5
        self.rect.y += (bullet_sizey * math.sin(rotationRobot2))*5


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

lastRotationRobot1 = None
lastRotationRobot2 = None


# -------- Main Program Loop -----------
while not gameExit:

    # ----- Game Over -----
    while gameOver == True:
        gameDisplay.fill(black)
        message_to_screen("Game over, press Start to play again or Q to quit", red, displaywidth/2 - 200, displayheight/2)

        screen_text = font.render("Green Score " + str(score), True, blue)
        gameDisplay.blit(screen_text, [displaywidth - 150, displayheight-580])

        screen_text = font.render("Blue Score " + str(score2), True, blue)
        gameDisplay.blit(screen_text, [displaywidth- 770, displayheight-580])
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

    #---Joystick Testing

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        name = joystick.get_name()
        axes = joystick.get_numaxes()

        for i in range( axes ):
            axis = joystick.get_axis( i )

        buttons = joystick.get_numbuttons()

        for i in range( buttons ):
            button = joystick.get_button( i )

    # ----- Event Processing  -----
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            gameExit = True

        elif event.type == pygame.JOYAXISMOTION:

            if event.axis == 1 or event.axis == 3:
                left = joystick.get_axis(1)
                right = joystick.get_axis(3)
                if abs(left) < 0.020:
                    left = 0

                if abs(right) < 0.020:
                    right = 0
                robots.setSpeed(0, left * -100, right * -100)


        elif event.type == pygame.JOYBUTTONDOWN:

            if event.button == 2:

                # Fire a bullet if the user hits the Blue 'X' Button
                bullet = Bullet()

                # Set the bullet so it is where the player is
                bullet.rect.x = centerRobot1[0] + rotatedPoint1[0]
                bullet.rect.y = centerRobot1[1] + rotatedPoint1[1]

                # Add the bullet to the lists
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)

            if event.button == 0:

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
                color = white
                circle.update()
                pygame.time.set_timer(RESETEVENT, 0)

        elif event.type == RESETEVENT2:
                color2 = white
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
    while(xS<=0 or yS<=0 or xB<=0 or yB<=0 or xS>=1 or yS>=1 or xB>=1 or yB>=1 ):
       ((xS,yS),(xB,yB)) = vision.robotLocation(1) #Triangle
    while(x1S<=0 or y1S<=0 or x1B<=0 or y1B<=0 or x1S>=1 or y1S>=1 or x1B>=1 or y1B>=1):
        ((x1S,y1S),(x1B,y1B)) = vision.robotLocation(2) #Quadrilateral


    testData = [[(xS, yS), (xB, yB)], [(x1S, y1S), (x1B, y1B)]]

    #Made testData below to test out bullets
    #testData2 = [[(0.5, 0.7), (0.5,0.8)], [(0.7, 0.7), (0.7, 0.8)]]
    testData = Line_Functions.convertVisionDataToScreenCoords(testData, displaywidth, displayheight)

    #Split Test Data into two robots
    robot1 = testData[0]
    robot2 = testData[1]

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

    #Determine the distence between the two given points
    distance1 = 60
        #math.sqrt((math.pow((robot1[1][0] - robot1[0][0]),2))+
         #                 (math.pow((robot1[1][1] - robot1[0][1]),2)))

    distance2 = 60
        #math.sqrt(math.pow((robot2[1][0] - robot2[0][0]),2)+
        #                 math.pow((robot2[1][1] - robot2[0][1]),2))

    rotatedPoint1 = [(math.cos(rotationRobot1) * distance1), (math.sin(rotationRobot1)* distance1)]
    rotatedPoint2 = [(math.cos(rotationRobot2) * distance2), (math.sin(rotationRobot2)* distance2)]

    #cos(angle)* radius of the circle, sin(angle)*radius of the circle
    #for orientation circle


    #
    #Boundaries of each tank
    #
    #Robot one, x then y
    if centerRobot1[0] + distance1 > displaywidth - 40.5 or centerRobot1[0] + distance1 < 0:
        tankleftx_c = 0
    if centerRobot1[1] + distance1 > displayheight - 20 or centerRobot1[1] + distance1 < 0:
        tanklefty_c = 0
    if centerRobot2[0] + distance2 > displaywidth - 40.5 or centerRobot2[0] + distance2 < displaywidth-850:
        tankrightx_c = 0
    if centerRobot2[1] + distance2 > displayheight - 20 or centerRobot2[1] + distance2 < displayheight-590:
        tankrighty_c = 0

    # Call the update() method on all the sprites
    all_sprites_list.update()
    circle.update()

    # Calculate collisions for bullets from player 1
    for bullet in bullet_list:

        # If player 2 is hit, remove the bullet, add to the player 1 score and turn the player 2 tank Blue 2
        if centerRobot2[0] + distance2 > bullet.rect.x > centerRobot2[0] - distance2 and centerRobot2[1] + distance2 > bullet.rect.y > centerRobot2[1] - distance2:
            color2 = blue
            circle2.timer()
            print "Hit green player"
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
            """
             if score <= 8.5 and score2 != -15:
                  score -= 0.1
               #print ("Tank 1 missed!")
            """



    # Calculate collisions for bullets from player 2
    for bullet2 in bullet2_list:

        # If the player 1 is hit, remove the bullet, add to the player 2 score and turn the player 1 tank Blue 2
        if centerRobot1[0] + distance1 > bullet2.rect.x > centerRobot1[0] - distance1 and centerRobot1[1] + distance1 > bullet2.rect.y > centerRobot1[1] - distance1:
            color = blue
            circle.timer()
            print "Hit blue player"
            bullet2_list.remove(bullet2)
            all_sprites_list.remove(bullet2)


            if score2 <= 8.5 and score != -15:
                score2+=1

            else:
                score2+=1
                gameOver = True

        # Remove the bullet if it flies up off the screen
        elif bullet2.rect.x > displaywidth + 10 or bullet2.rect.y > displayheight + 10 or bullet2.rect.x < -5 or bullet2.rect.y < -5:
            bullet2_list.remove(bullet2)
            all_sprites_list.remove(bullet2)

            #Use the code below to penalize tank 2 for missing after shooting
            """
            if score2 <= 8.5 and score != -15:
                score2 -= 0.1
                #print ("Tank 2 missed!")
            """

    # --- Draw a frame

    # Clear the screen
    gameDisplay.fill(black)

    wallx = 170; wally = 110; wallwidth = 10; wallheight = 290;
    wallx2 = displaywidth/2; wally2 = 0; wallheight2 = 80

    upper = 10; lower = 5; upper2 = upper; lower2 = lower;

    #Draw Walls
    wall = pygame.draw.rect(gameDisplay, white, (wallx, wally, wallwidth, wallheight), 0)
    wall2 = pygame.draw.rect(gameDisplay, white, (displaywidth-wallx, wally, wallwidth, wallheight), 0)

    wall3 = pygame.draw.rect(gameDisplay, white, (wallx2, wally2, wallwidth, wallheight2), 0)
    wall4 = pygame.draw.rect(gameDisplay, white, (wallx2, displayheight-wally2-wallheight2, wallwidth, wallheight2), 0)

    #wall5 = pygame.draw.rect(gameDisplay, white, (wallx2-60, displayheight/2, 140, wallwidth), 0)
    """"
    #Wall 1

    #Right side of wall 1
    if centerRobot1[0] - distance1 >= wallx + lower and centerRobot1[0] - distance1 <= wallx + upper:
        #right = 0;
        color = blue
        print "Player 1 near right side wall 1"

    if centerRobot2[0] - distance2 <= wallx + upper and centerRobot2[0] - distance2 >= wallx + lower:
        #right = 0;
        color2 = blue
        print "Player 2 near right side wall 1"

    #Left side wall 1
    if centerRobot1[0] + distance1 >= wallx - upper and centerRobot1[0] + distance1 <= wallx - lower:
        #left = 0;
        color = green
        print "Player 1 near left side wall 1"

    if centerRobot2[0] + distance2 >= wallx - upper and centerRobot2[0] + distance2 <= wallx - lower:
        #left = 0;
        color2 = green
        print "Player 2 near left side wall 1"

    #Wall 2

    #Right side of wall 2
    if centerRobot1[0] - distance1 <= displaywidth - wallx + upper2 and centerRobot1[0] - distance1 >= displaywidth - wallx + lower2:
        #right = 0;
        print "Player 1 near right side wall 2"
        color = red

    if centerRobot2[0] - distance2 <= displaywidth - wallx + upper2 and centerRobot2[0] - distance2 >= displaywidth - wallx + lower2:
        #right = 0;
        print "Player 2 near right side wall 2"
        color2 = red

    #Left side of wall 2
    if centerRobot1[0] + distance1 >= displaywidth - wallx - upper2 and centerRobot1[0] + distance1 <= displaywidth - wallx - lower2:
        #left = 0;
        print "Player 1 near left side wall 2"
        color = blue

    if centerRobot2[0] + distance2 >= displaywidth - wallx - upper2 and centerRobot2[0] + distance2 <= displaywidth - wallx - lower2:
        #left = 0;
        print "Player 2 near left side wall 2"
        color2 = blue
    """

    # Draw all the spites
    all_sprites_list.draw(gameDisplay)
    circle.update()
    circle2.update()
    
    #Draw Orientation Points
    pygame.draw.circle(gameDisplay, blue2,( int(rotatedPoint1[0] + centerRobot1[0] + 10), int(rotatedPoint1[1]+ centerRobot1[1] + 10)), 10, 0)
    pygame.draw.circle(gameDisplay, blue2,( int(rotatedPoint2[0] + centerRobot2[0] + 2),  int(rotatedPoint2[1] + centerRobot2[1] + 2 )), 10, 0)
    
    #Draw scores in the top corners
    screen_text = font.render("Triangle Score " + str(score), True, red)
    gameDisplay.blit(screen_text, [displaywidth - 150, displayheight - 480])

    screen_text = font.render("Square Score " + str(score2), True, red)
    gameDisplay.blit(screen_text, [displaywidth - 710, displayheight - 480])

    
    #Update the screen
    pygame.display.flip()
    
    # --- Limit to frames per second
    clock.tick(FPS)

    
pygame.quit()
sys.exit()
quit()


