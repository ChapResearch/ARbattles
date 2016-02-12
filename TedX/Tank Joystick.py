import pygame
import time
import math
import sys
import Line_Functions
import Movement

'''
from robotControl import robotControl

robots = robotControl(3)
'''

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
block_size = 10;

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

circle_radius = int(distance1)

color = blue
color2 = white

#-----Classes-----

#----Tank Circle Classes----

class Circle (pygame.sprite.Sprite):
    global x1, y1, distance1, time, RESETEVENT
    # This class represents the orientation of the tank.
    
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((distance1,distance1))
        self.image.fill(blue2)
        
        pygame.draw.circle(gameDisplay, color,(x1, y1), int(distance1), 0)
        
        self.rect = self.image.get_rect()
        
    def update(self):
        # Update
        self.rect.x = x1-distance1
        self.rect.y = y1-distance1
        pygame.draw.circle(gameDisplay, color,(x1, y1), int(distance1), 0)

    def timer(self):
        pygame.time.set_timer(RESETEVENT, time)
        


class Circle2 (pygame.sprite.Sprite):
    global x2, y2, distance2, time, RESETEVENT2
    # This class represents the orientation of the tank.
    
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((distance2,distance2))
        self.image.fill(blue)
        pygame.draw.circle(gameDisplay, color2,(x2, y2), int(distance2), 0)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

        self.rect = self.image.get_rect()
        
    def update(self):
    #   Update
        self.rect.x = x2-distance2
        self.rect.y = y2-distance2
        pygame.draw.circle(gameDisplay, color2,(x2, y2), int(distance2), 0)

    def timer(self):
        pygame.time.set_timer(RESETEVENT2, time)


        
#-----Bullet Classes-----
class Bullet (pygame.sprite.Sprite):
    global bullet_sizex, bullet_sizey, color
    """ This class represents the missile for the Green Tank. """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Bullet, self).__init__()
 
        self.image = pygame.Surface([bullet_sizex, bullet_sizey])
        self.image.fill(color)
 
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Move the bullet. """
        self.rect.x += bullet_sizex * math.cos(rotationRobot1)
        self.rect.y += bullet_sizey * math.sin(rotationRobot1)
            
class Bullet2 (pygame.sprite.Sprite):
    """ This class represents the missile for the Blue Tank. """
    global bullet_sizex, bullet_sizey, color2
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Bullet2, self).__init__()

 
        self.image = pygame.Surface([bullet_sizex, bullet_sizey])
        self.image.fill(color2)
 
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Move the bullet. """
        self.rect.x += bullet_sizex * math.cos(rotationRobot2)
        self.rect.y += bullet_sizey * math.sin(rotationRobot2)


#--Method to print text on screen
def message_to_screen(msg, color, xpos, ypos):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [xpos, ypos])

# --- Create the window
 
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

hello = True





# -------- Main Program Loop -----------
while not gameExit:
    
    # ----- Game Over -----    
    while gameOver == True:
        gameDisplay.fill(black)
        message_to_screen("Game over, press Start to play again or Q to quit", red, displaywidth/2 - 200, displayheight/2)

        screen_text = font.render("Green Score " + str(score), True, red)
        gameDisplay.blit(screen_text, [displaywidth - 150, displayheight-580])

        screen_text = font.render("Blue Score " + str(score2), True, red)
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
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    joystick2 = pygame.joystick.Joystick(1)
    joystick2.init()
    
            
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
                #robots.setSpeed(0, left * -100, right * -100)

            
        elif event.type == pygame.JOYBUTTONDOWN:

            if joystick.get_button(0):
                
                # Fire a bullet if the user hits the Blue 'X' Button
                bullet = Bullet()
                
                # Set the bullet so it is where the player is
                bullet.rect.x = centerRobot1[0] + rotatedPoint1[0]
                bullet.rect.y = centerRobot1[1] + rotatedPoint1[1]
                
                # Add the bullet to the lists
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)
            
            if joystick2.get_button(0):
                
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
                print "Player 1 Event"
                color = blue
                circle.update()
                pygame.time.set_timer(RESETEVENT, 0)
                
        elif event.type == RESETEVENT2:
                print "Player 2 Event"
                color2 = red
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
    testData = [[(0.25, 0.25), (0.3, 0.3)], [(0.7, 0.7), (0.7, 0.8)]]

    #Made testData below to test out bullets
    testData2 = [[(0.5, 0.7), (0.5,0.8)], [(0.7, 0.7), (0.7, 0.8)]]
    testData = Line_Functions.convertVisionDataToScreenCoords(testData, displaywidth, displayheight)

    #testData = [[(Robot 1)(x1, y1), (x2, y2)], [(Robot 2)(x1, y1), (x2, y2)]]

    #Split Test Data into two robots
    robot1 = testData[0] #[(0.25, 0.25), (0.3,0.3)]
    robot2 = testData[1] #[(0.7, 0.7), (0.7, 0.8)]

    #Find centers
    centerRobot1 = Line_Functions.centerOfLine(robot1[0], robot1[1])
    centerRobot2 = Line_Functions.centerOfLine(robot2[0], robot2[1])

    x1 = int(centerRobot1[0]); y1 = int(centerRobot1[1]); x2 = int(centerRobot2[0]); y2 = int(centerRobot2[1])
    
    #Determine the distence between the two given points
    distance1 = int(60)
    distance2 = int(60)
    
    #Determine the degrees the robot is facing from east    
    rotationRobot1 = Line_Functions.rotationOfLine(robot1[0], robot1[1])
    rotationRobot2 = Line_Functions.rotationOfLine(robot2[0], robot2[1])

    rotatedPoint1 = [(math.cos(rotationRobot1) * distance1), (math.sin(rotationRobot1)* distance1)]
    rotatedPoint2 = [(math.cos(rotationRobot2) * distance2), (math.sin(rotationRobot2)* distance2)]
    
    
    #cos(angle)* radius of the circle, sin(angle)*radius of the circle
    #for orientation circle

    

    ##
    #Boundaries of each tank
    ##

    #Left Boundary
    #if centerRobot1[0] - distance1 < 100:
    #    print "Robot 1 Left Wall"
    
    if hello == True:
        Movement.startBounce(1)
        hello = False
        
    Movement.doAuto()  
    
    #Right Boundary
    if centerRobot1[0] + distance1 > displaywidth - 40.5:
        left = 0
        #color = green

    #Top Boundary
    if centerRobot1[1] + distance1 < 10:
        left = 0 ###CHANGE THIS###
        #color = blue

    #Bottom Boundary
    if centerRobot1[1] + distance1 > displayheight - 20:
        right = 0 ###CHANGE THIS###
        #color = green2

    ###Robot 2###
    #Left Boundary
    if centerRobot2[0] + distance2 < displaywidth-850:
        right2 = 0

    #Right Boundary
    if centerRobot2[0] + distance2 > displaywidth - 40.5:
        left2 = 0

    #Bottom Boundary
    if centerRobot2[1] + distance2 > displayheight - 20:
        right = 0 ###CHANGE THIS###

    #Top Boundary
    if centerRobot2[1] + distance2 < displayheight-590:
        left = 0 #CHANGE THIS###
    #
    #
    #

    # Call the update() method on all the sprites
    all_sprites_list.update()
    circle.update()
    
    # Calculate collisions for bullets from player 1
    for bullet in bullet_list:
        
        # If player 2 is hit, remove the bullet, add to the player 1 score and turn the player 2 tank Blue 2
        if centerRobot2[0] + distance2 > bullet.rect.x > centerRobot2[0] - distance2 and centerRobot2[1] + distance2 > bullet.rect.y > centerRobot2[1] - distance2:
            color2 = blue2
            circle2.timer()
            print "Hit red player"
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
            color = blue2
            circle.timer()
            print "Hit blue player"
            bullet2_list.remove(bullet2)
            all_sprites_list.remove(bullet2)


            if score2 <= 8.5 and score != -15:
                score2+=1
                
            else:
                score2+=1
                gameOver = True
                
            #print "Score 2: ", score2, "\n"

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

    wallx = 170; wally = 120; wallwidth = 10; wallheight = 270;
    wallx2 = displaywidth/2; wally2 = 0; wallheight2 = 80

    upper = 10; lower = 10; upper2 = upper; lower2 = lower;

    #Draw Walls
    wall = pygame.draw.rect(gameDisplay, white, (wallx, wally, wallwidth, wallheight), 0)
    wall2 = pygame.draw.rect(gameDisplay, white, (displaywidth-wallx, wally, wallwidth, wallheight), 0)

    wall3 = pygame.draw.rect(gameDisplay, white, (wallx2, wally2, wallwidth, wallheight2), 0)
    wall4 = pygame.draw.rect(gameDisplay, white, (wallx2, displayheight-wally2-wallheight2, wallwidth, wallheight2), 0)

    #wall5 = pygame.draw.rect(gameDisplay, white, (wallx2-60, displayheight/2, 140, wallwidth), 0)


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
    ####ORIGINAL######
    wallx = 150; wally = 100; wallwidth = 10; wallheight = 300;
    wallx2 = displaywidth/2; wally2 = 0; wallheight2 = 80

    upper = 10; lower = 5; upper2 = upper; lower2 = lower;

    #Draw Walls
    wall = pygame.draw.rect(gameDisplay, white, (wallx, wally, wallwidth, wallheight), 0)
    wall2 = pygame.draw.rect(gameDisplay, white, (displaywidth-wallx, wally, wallwidth, wallheight), 0)
    
    wall3 = pygame.draw.rect(gameDisplay, white, (wallx2, wally2, wallwidth, wallheight2), 0)
    wall4 = pygame.draw.rect(gameDisplay, white, (wallx2, displayheight-wally2-wallheight2, wallwidth, wallheight2), 0)

    wall5 = pygame.draw.rect(gameDisplay, white, (wallx2-60, displayheight/2, 140, wallwidth), 0)

    #Wall 1

    #On right side of wall 1
    if (centerRobot1[0] - distance1 >= wallx + lower and centerRobot1[0] - distance1 <= wallx + upper):
        #right = 0;
        color = green
        print "Player 1 near right side wall 1"
        
    if (centerRobot2[0] - distance2 <= wallx + upper and centerRobot2[0] - distance2 >= wallx + lower):
        #right = 0;
        color2 = blue
        print "Player 2 near right side wall 1"

    #left side wall 1
    if (centerRobot1[0] + distance1 >= wallx - upper and centerRobot1[0] + distance1 <= wallx - lower):
        #left = 0;
        color = green
        print "Player 1 near left side wall 1"
        
    if (centerRobot2[0] + distance2 >= wallx - upper and centerRobot2[0] + distance2 <= wallx - lower):
        #left = 0;
        color2 = blue
        print "Player 2 near left side wall 1"

        
    #Wall 2

    #On right side of wall 2
    if (centerRobot1[0] - distance1 <= displaywidth - wallx + upper2 and centerRobot1[0] - distance1 >= displaywidth - wallx + lower2):
        #right = 0;
        color = green
        
    if (centerRobot2[0] - distance2 <= displaywidth - wallx + upper2 and centerRobot2[0] - distance2 >= displaywidth - wallx + lower2):
        #right = 0;
        color2 = blue
        
    #On left side of wall 1
    if (centerRobot1[0] + distance1 >= displaywidth - wallx - upper2 and centerRobot1[0] + distance1 <= displaywidth - wallx - lower2):
        #right = 0;
        color = green
        
    if (centerRobot2[0] + distance2 >= displaywidth - wallx - upper2 and centerRobot2[0] + distance2 <= displaywidth - wallx - lower2):
        #right = 0;
        color2 = blue
    """ 
    # Draw all the spites
    all_sprites_list.draw(gameDisplay)
    circle.update()
    circle2.update()
    
    #Draw Orientation Points
    pygame.draw.circle(gameDisplay, blue2,(int(rotatedPoint1[0] + centerRobot1[0]), int(rotatedPoint1[1]+ centerRobot1[1])), 15, 0)
    pygame.draw.circle(gameDisplay, blue2,(int(rotatedPoint2[0] + centerRobot2[0]), int(rotatedPoint2[1] + centerRobot2[1])), 15, 0)
    
    #Print scores in the top corners
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


