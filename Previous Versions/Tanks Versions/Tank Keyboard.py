import pygame
import time
import math
#import cv2
#import numpy as np

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

player_sizex = 30
player_sizey = 30

bullet_sizex = 20
bullet_sizey = 8

#events to reset color after a hit
RESETEVENT = pygame.USEREVENT + 1
RESETEVENT2 = pygame.USEREVENT + 1
time = 700

blue_tank = pygame.image.load("tanks/blue_tank.png")
green_tank = pygame.image.load("tanks/green_tank.png")

num = -1
num2 = -1

rotate1 = False
temp = pygame.image.load("tanks/green_tank.png")

rotate2 = False
temp2 = pygame.image.load("tanks/blue_tank.png")

degrees = 0
degrees2 = 0

#-----Classes-----


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
        
        self.image = pygame.image.load("tanks/green_tank.png")
        
 
        self.rect = self.image.get_rect()
        
    def update(self):
        """ Update the player's position. """
        global tankleftx, tanklefty
        
        # Set the player x and y positions to the variables
        self.rect.x = tankleftx
        self.rect.y = tanklefty
        
    def rotate(self, angle):
        rotate1 = True
        self.image = pygame.transform.rotate(self.image, angle)

    def timer(self):
        pygame.time.set_timer(RESETEVENT, time)
        
    def restore (self):
        if (rotate1 == False ):
            self.image = pygame.image.load("tanks/green_tank.png")
            degrees = 0;
            num = 0
            print "Player 1 restore num and degrees", num, degrees
            
        else:
            self.image = temp
            print "player 1 else"
        
    def hit(self):
        #Turn to red because player 2 was hit
        self.image = pygame.image.load("tanks/green_hit.png")
        
        
class Player2(pygame.sprite.Sprite):
    """ This class represents the Blue Player. """
    global RESETEVENT, time, player_sizex, player_sizey, rotate2, temp2, degrees2, num2

    def __init__(self):
        """ Set up the player on creation. """
        
        # Call the parent class (Sprite) constructor
        super(Player2,self).__init__()
        self.image = pygame.image.load("tanks/blue_tank.png")
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
            self.image = pygame.image.load("tanks/blue_tank.png")
            
        else:
            self.image = temp2
            print "player 2 else"
        
    def hit(self):
        #Turn to red because player 2 was hit
        self.image = pygame.image.load("tanks/blue_hit.png")
        degrees2 = 0
        num2 = 0
        print "Hit Num 2 and degrees 2", num2, degrees2
    print "Outside method num 2 and degrees", num2, degrees


# --- Create the window
 
# Set the height and width of the display
displaywidth = 800
displayheight = 600
gameDisplay = pygame.display.set_mode([displaywidth, displayheight])
pygame.display.set_caption('Tank Game')          


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


tankrightx = displaywidth/2 - 120
tankrighty = displayheight/2-10


player.rect.y = displayheight-30

hit = False
hit2 = False


# -------- Main Program Loop -----------
while not gameExit:
    
    # ----- Game Over -----    
    while gameOver == True:
        gameDisplay.fill(blue2)
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
                

    # ----- Event Processing  -----   
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            gameExit = True          


    
    #Boundaries of each tank         
    if tankleftx > displaywidth - 40.5 or tankleftx < displaywidth-850:
        tankleftx_c = 0
    if tanklefty > displayheight - 20 or tanklefty < 0:
        tanklefty_c = 0
    if tankrightx > displaywidth - 40.5 or tankrightx < displaywidth-850:
        tankrightx_c = 0
    if tankrighty > displayheight - 20 or tankrighty < displayheight-590:
        tankrighty_c = 0
        
    #Take the change and add it to the tank's position
    ##tankleftx += tankleftx_c
    ##tanklefty += tanklefty_c
    
    ##tankrightx += tankrightx_c
    ##tankrighty += tankrighty_c
    

    # --- Game logic
    
    # Call the update() method on all the sprites
    all_sprites_list.update()

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
    gameDisplay.fill(blue2)
 
    # Draw all the spites
    all_sprites_list.draw(gameDisplay)

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


