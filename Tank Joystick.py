import pygame
import time
import math
#import cv2
#import numpy as np
#hello

pygame.init()

# Define Colors
white = (255, 255, 255)
WHITE = (255, 255, 255)

black = (0, 0, 0)
BLACK = (0, 0, 0)

RED = (255, 0, 0)        #hit tank
red = (255, 0, 0)
red2 = (220, 0, 0)

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

bullet_sizex = 20
bullet_sizey = 8

circle_radius = 6

#events to reset color after a hit
RESETEVENT = pygame.USEREVENT + 1
RESETEVENT2 = pygame.USEREVENT + 1
time = 700

num = -1
num2 = -1

rotate1 = False


rotate2 = False
degrees = 0
degrees2 = 0

#-----Classes-----

#----Circle Class---
class Circle (pygame.sprite.Sprite):
    global tankrightx, tankrighty, circle_radius
    # This class represents the orientation of the tank.
    
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill(blue2)
        
        pygame.draw.circle(player.image, white, (player_sizex/2, 10 ), circle_radius, 0)
        
        self.rect = self.image.get_rect()
        
    def update(self):
    #   Function unknown
        pygame.draw.circle(player.image, white, (player_sizex/2, 10 ), circle_radius, 0)

    
class Circle2 (pygame.sprite.Sprite):
    global tankrightx, tankrighty, circle_radius
    # This class represents the orientation of the tank.
    
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,20))
        self.image.fill(blue)
        pygame.draw.circle(player2.image, white, (player_sizex/2, 10 ), circle_radius, 0)
        self.rect = self.image.get_rect()
        
    def update(self):
    #   Function unknown
        pygame.draw.circle(player2.image, white, (player_sizex/2, 10 ), circle_radius, 0)


        
#-----Bullet Classes-----
class Bullet (pygame.sprite.Sprite):
    global bullet_sizex, bullet_sizey, num
    """ This class represents the missile for the Green Tank. """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Bullet, self).__init__()
 
        self.image = pygame.Surface([bullet_sizex, bullet_sizey])
        self.image.fill(green)
 
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Move the bullet. """
        if num == 0:
            self.rect.x -= bullet_sizex

        elif num == 1:
            self.image = pygame.Surface([bullet_sizey, bullet_sizex])
            self.image.fill(green)
            
            self.rect.y -= bullet_sizex

        elif num == 2:
            self.rect.x += bullet_sizex
            
        elif num == 3:
            
            self.image = pygame.Surface([bullet_sizey, bullet_sizex])
            self.image.fill(green)
            
            self.rect.y += bullet_sizex

        elif num == -1:
            print "Fail player 1"
            
class Bullet2 (pygame.sprite.Sprite):
    """ This class represents the missile for the Blue Tank. """
    global bullet_sizex, bullet_sizey, num2
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Bullet2, self).__init__()

 
        self.image = pygame.Surface([bullet_sizex, bullet_sizey])
        self.image.fill(blue)
 
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Move the bullet. """
        print "Bullet num 2", num2
        
        if num2 == 0:
            self.rect.x += bullet_sizex

        elif num2 == 1:
            self.image = pygame.Surface([bullet_sizey, bullet_sizex])
            self.image.fill(blue)
            
            self.rect.y -= bullet_sizex

        elif num2 == 2:
            self.rect.x -= bullet_sizex
            
        elif num2 == 3:
            
            self.image = pygame.Surface([bullet_sizey, bullet_sizex])
            self.image.fill(blue)
            
            self.rect.y += bullet_sizex 

        elif num2 == -1:
            print "Fail player 2"


#----Tank Classes-----

class Player(pygame.sprite.Sprite):
    """ This class represents the Green Player. """
    global RESETEVENT, time, player_sizex, player_sizey, rotate1, temp, degrees, num

    def __init__(self):
        """ Set up the player on creation. """
        
        # Call the parent class (Sprite) constructor
        super(Player,self).__init__()
        
        self.image = pygame.Surface([player_sizex, player_sizey])
        self.image.fill(green)
        
        self.rect = self.image.get_rect()
        
    def update(self):
        """ Update the player's position. """
        global tankleftx, tanklefty
        
        # Set the player x and y positions to the variables
        self.rect.x = tankleftx
        self.rect.y = tanklefty
        
    def rotate(self,angle):
        """
        r = rotations.get(gameObject,0) + 45
        rotations[gameObject] = r
        return pygame.transform.rotate(gameObject, r)
        """
        rotate1 = True
        self.image = pygame.transform.rotate(self.image, angle)
    def timer(self):
        pygame.time.set_timer(RESETEVENT, time)
        
    def restore (self):
        if (rotate1 == False ):
            self.image.fill(green)
            
            degrees = 0;
            num = 0
            print "Player 1 restore num and degrees", num, degrees
            
        else:
            print "player 1 else"
            
    def hit(self):
        #Turn to red because player 2 was hit
        self.image = pygame.Surface([player_sizex, player_sizey])
        self.image.fill(red)
        
        
class Player2(pygame.sprite.Sprite):
    """ This class represents the Blue Player. """
    global RESETEVENT, time, player_sizex, player_sizey, rotate2, temp2, degrees2, num2

    def __init__(self):
        """ Set up the player on creation. """
        
        # Call the parent class (Sprite) constructor
        super(Player2,self).__init__()
        self.image = pygame.Surface([player_sizex,player_sizey])
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        
        
    def update(self):
        """ Update the player's position. """
        global tankrightx, tankrighty
        
        # Set the player x and y positions to the variables
        self.rect.x = tankrightx
        self.rect.y = tankrighty
        
    def rotate(self, angle):
        rotate2 = True
        self.image = pygame.transform.rotate(self.image, angle)

    def timer(self):
        pygame.time.set_timer(RESETEVENT, time)
        
    def restore (self):
        if (rotate2 == False ):
            self.image.fill(blue)
            
        else:
            print "player 2 else"
        
    def hit(self):
        #Turn to red because player 2 was hit
        self.image.fill(red)
        degrees2 = 0
        num2 = 0
        print "Hit Num 2 and degrees 2", num2, degrees2

    
# --- Create the window
 
# Set the height and width of the display
displaywidth = 800
displayheight = 600
gameDisplay = pygame.display.set_mode([displaywidth, displayheight])
pygame.display.set_caption('Tank Game')          


#--Method to print text on screen --not used--
def message_to_screen(msg, color, xpos, ypos):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [xpos, ypos])


# --- Sprite lists
 
# This is a list of every sprite (player and missiles)
all_sprites_list = pygame.sprite.Group()

 
# List of each bullet
bullet_list = pygame.sprite.Group()
bullet2_list = pygame.sprite.Group()


# Create a player tanks

#Player 1
player = Player()
all_sprites_list.add(player)

#Player 2
player2 = Player2()
all_sprites_list.add(player2)


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

player.rect.y = displayheight-30

hit = False
hit2 = False

#Circle 1
circle = Circle()
all_sprites_list.add(circle)

#Circle 2
circle2 = Circle2()
all_sprites_list.add(circle2)



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

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
            if event.axis == 0:
                if joystick.get_axis(0) > 0.02:
                    #not used
                    tankrightx_c += block_size

                elif joystick.get_axis(0) < -0.020:
                    #not used
                    tankrightx_c -= block_size
                    
                elif joystick.get_axis(0) < 0.020 and joystick.get_axis(0) > -0.020:
                    #not used
                    tankrightx_c = 0

                
            elif event.axis == 1:
                if joystick.get_axis(1) > 0.020:
                    #move forward left servo robot 1 
                    tankrighty_c += block_size
                    
                elif joystick.get_axis(1) < -0.020:
                    #move backward left servo robot 1
                    tankrighty_c -= block_size
                    
                elif joystick.get_axis(1) < 0.020 and joystick.get_axis(1) > -0.020:
                    #stop left servo robot 1
                    tankrighty_c = 0
                  

            if event.axis == 2:
                if joystick.get_axis(2) > 0.020:
                    #not used
                    tankleftx_c += block_size
                    
                elif joystick.get_axis(2) < -0.020:
                    #not used
                    tankleftx_c -= block_size
                    
                elif joystick.get_axis(2) < 0.020 and joystick.get_axis(2) > -0.020:
                    #not used
                    tankleftx_c = 0
                
               
            elif event.axis == 3:
                if joystick.get_axis(3) > 0.020:
                    #forward right servo robot 1
                    tanklefty_c += block_size
                    
                elif joystick.get_axis(3) < -0.020:
                    #backward right servo robot 1
                    tanklefty_c -= block_size
                
                elif joystick.get_axis(2) < 0.020 and joystick.get_axis(2) > -0.020:
                    #stop right servo robot 1
                    tanklefty_c = 0

        
        elif event.type == pygame.JOYBUTTONDOWN:
        
            if event.button == 4:
                
                if hit2 == False:
                    
                    player2.rotate(90)
                
                    if degrees2 != 270:
                        degrees2 += 90
                    
                    else:
                        degrees2 = 0
                else:
                     print "Left Player has been hit!"
                     #degrees2 = 90
                     hit2 = False
                     
                print "Player 2: ", degrees2
                #print "turn"
                
            if event.button == 6:
                if hit2 == False:                    
                    player2.rotate(-90)

                    if degrees2 != -270:
                        degrees2 -= 90
                        
                    else:
                        degrees2 = 0
                else:
                     print "Left Player has been hit!"
                     #degrees2 = -90
                     hit2 = False
                    
                print "Player 2: ", degrees2
                #print "turn other way"
                    
                
            if event.button == 5:
                if hit == False:
                    player.rotate(90)
                    
                    if degrees != 270:
                        degrees += 90
                        
                    else:
                        degrees = 0
                else:
                     print "Right player has been hit!"
                     player.rotate(90)
                     degrees += 90
                     hit = False
                #print "turn 2"
                print "Player 1: ", degrees
                
            if event.button == 7:
                if hit == False:
                    player.rotate(-90)
                    
                    if degrees != -270:
                        degrees -= 90
                        
                    else:
                        degrees = 0
                else:
                     print "Right Player has been hit!"
                     degrees += -90
                     player.rotate(-90)
                     hit = False
                #print "turn other way 2"
                print "Player 1: ", degrees
                
            if event.button == 0:
                
                # Fire a bullet if the user hits the right bumper
                bullet2 = Bullet2()
                # Set the bullet so it is where the player is
                
                if  (degrees2 == 0):
                    bullet2.rect.x = player2.rect.x + 85
                    bullet2.rect.y = player2.rect.y + 9
                    num2 = 0
                    
                elif (degrees2 == 90 or degrees2 == -270):
                    bullet2.rect.x = player2.rect.x + 8
                    bullet2.rect.y = player2.rect.y + 20
                    num2 = 1
                    
                elif (degrees2 == 180 or degrees2 == -180):
                    bullet2.rect.x = player2.rect.x + 10
                    bullet2.rect.y = player2.rect.y + 45
                    num2 = 2
                    
                elif (degrees2 == 270 or degrees2 == -90 ):
                    bullet2.rect.x = player2.rect.x + 45
                    bullet2.rect.y = player2.rect.y + 80
                    num2 = 3
                    

                else:
                    print "angle is not working player 2"

                
                # Add the bullet to the lists
                all_sprites_list.add(bullet2)
                bullet2_list.add(bullet2)
                
            if event.button == 2:
                print degrees
                
                # Fire a bullet if the user hits the Space Bar
                bullet = Bullet()
                
                # Set the bullet so it is where the player's turret is
                if (degrees == 0):
                    bullet.rect.x = player.rect.x + 10
                    bullet.rect.y = player.rect.y + 9
                    num = 0
                    
                elif (degrees == -90 or degrees == 270):
                    bullet.rect.x = player.rect.x + 50
                    bullet.rect.y = player.rect.y
                    num = 1

                elif (degrees == 180 or degrees == -180):
                    bullet.rect.x = player.rect.x + 50
                    bullet.rect.y = player.rect.y + 50
                    num = 2

                elif ( degrees == -270 or degrees == 90 ):
                    bullet.rect.x = player.rect.x + 10
                    bullet.rect.y = player.rect.y + 9
                    num = 3

                else:
                    print "angle is not woking player 1"
                    
                # Add the bullet to the lists
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)
                
        #Reset the tanks back to their original color        
        if event.type == RESETEVENT:
                #print "Player 1 Hit"
                player.restore()
                circle.update()
                pygame.time.set_timer(RESETEVENT, 0)
                
        if event.type == RESETEVENT2:
                #print "Player 2 Hit"
                player2.restore()
                circle.update()
                pygame.time.set_timer(RESETEVENT2, 0)
                


    
    #Boundaries of each tank         
    if tankleftx + tankleftx_c > displaywidth - 40.5 or tankleftx + tankleftx_c < displaywidth-1050:
        tankleftx_c = 0
    if tanklefty + tanklefty_c > displayheight - 20 or tanklefty + tanklefty_c < 0:
        tanklefty_c = 0
    if tankrightx + tankrightx_c > displaywidth - 40.5 or tankrightx + tankrightx_c < displaywidth-850:
        tankrightx_c = 0
    if tankrighty + tankrighty_c > displayheight - 20 or tankrighty + tankrighty_c < displayheight-590:
        tankrighty_c = 0
        
    #Take the change and add it to the tank's position
    tankleftx += tankleftx_c
    tanklefty += tanklefty_c
    
    tankrightx += tankrightx_c
    tankrighty += tankrighty_c
    

    # --- Game logic
    
    #Call CV Method
    #tuple = given value
    #tuple[0] = x position
    #tuple[1] = y position
    #tuple[2] = x of end
    #tuple[3] = y of end

    #cos(angle)* radius of the circle, sin(angle)*radius of the circle
    #for orientation circle

    
    # Call the update() method on all the sprites
    all_sprites_list.update()
    #circle.update(tankrightx,tankrighty)
    
    # Calculate collisions for bullets from player 1
    for bullet in bullet_list:
        
        # If player 2 is hit, remove the bullet, add to the player 1 score and turn the player 2 tank red
        if player2.rect.x + 80 > bullet.rect.x > player2.rect.x - 20 and player2.rect.y + 50 > bullet.rect.y > player2.rect.y - 20:
            player2.hit()
            hit2 = True
            player2.timer()
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
                
            """Use the code below to penalize tank 1 for missing after shooting"""
            #  if score <= 8.5 and score2 != -15:
            #      score -= 0.1
               #print ("Tank 1 missed!")

            
          
    # Calculate collisions for bullets from player 2
    for bullet2 in bullet2_list:
        
        # If the player 1 is hit, remove the bullet and add to the player 2 score   
        if player.rect.x + 20 > bullet2.rect.x > player.rect.x - 20 and player.rect.y + 50 > bullet2.rect.y > player.rect.y - 20:
            player.hit()
            hit = True
            player.timer()
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

            """Use the code below to penalize tank 2 for missing after shooting""" 
            #if score2 <= 8.5 and score != -15:
            #    score2 -= 0.1
                #print ("Tank 2 missed!")

    # --- Draw a frame
    
    # Clear the screen
    gameDisplay.fill(black)
 
    # Draw all the spites
    all_sprites_list.draw(gameDisplay)
    #circle.draw(gameDisplay)

    # Extra Game Elements

    #middle dividing line
    #pygame.draw.rect(gameDisplay, black, [displaywidth/2,displayheight-600 , 5, displayheight])

    #Print scores in the top corners
    screen_text = font.render("Green Score " + str(score), True, red)
    gameDisplay.blit(screen_text, [displaywidth - 150, displayheight-580])

    screen_text = font.render("Blue Score " + str(score2), True, red)
    gameDisplay.blit(screen_text, [displaywidth- 770, displayheight-580])

    #Update the screen
    pygame.display.flip()
    
    # --- Limit to frames per second
    clock.tick(FPS)

    
pygame.quit()
quit()


