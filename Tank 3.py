import pygame
import time

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
block_size = 30;

player_sizex = 30
player_sizey = 30

bullet_sizex = 20
bullet_sizey = 8

#events to reset color after a hit
RESETEVENT = pygame.USEREVENT + 1
RESETEVENT2 = pygame.USEREVENT + 1
time = 700

#import image
#image3 = pygame.image.load("tanks/tank1.png")
blue_tank = pygame.image.load("tanks/blue_tank.png")


#-----Classes-----

#-----Bullet Classes-----
class Bullet (pygame.sprite.Sprite):
    global bullet_sizex, bullet_sizey
    """ This class represents the missile for the Green Tank. """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Bullet, self).__init__()
 
        self.image = pygame.Surface([bullet_sizex, bullet_sizey])
        self.image.fill(green)
 
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Move the bullet. """
        self.rect.x -= bullet_sizex


class Bullet2 (pygame.sprite.Sprite):
    """ This class represents the missile for the Blue Tank. """
    global bullet_sizex, bullet_sizey
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Bullet2, self).__init__()
 
        self.image = pygame.Surface([bullet_sizex, bullet_sizey])
        self.image.fill(blue)
 
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Move the bullet. """
        self.rect.x += bullet_sizex



#----Tank Classes-----
class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """
    global RESETEVENT2, time, player_sizex, player_sizey 
    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super(Player,self).__init__()
 
        self.image = pygame.image.load("tanks/green_tank.png")
        #self.image.fill(green)
 
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Update the player's position. """
        global tankleftx, tanklefty
        
        # Set the player x and y positions to the variables
        self.rect.x = tankleftx
        self.rect.y = tanklefty
        
    def timer(self):
        pygame.time.set_timer(RESETEVENT2, time)
        
    def restore (self):
        #Restore back to green
        self.image = pygame.image.load("tanks/green_tank.png")

        
    def hit(self):
        #Turn to red because player 1 was hit
        self.image = pygame.image.load("tanks/green_hit.png")

        
 
class Player2(pygame.sprite.Sprite):
    """ This class represents the Blue Player. """
    global RESETEVENT, time, player_sizex, player_sizey, blue_tank
    def __init__(self):
        """ Set up the player on creation. """
        
        # Call the parent class (Sprite) constructor
        super(Player2,self).__init__()
 
        self.image = blue_tank
 
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Update the player's position. """
        global tankrightx, tankrighty
        
        # Set the player x and y positions to the variables
        self.rect.x = tankrightx
        self.rect.y = tankrighty
        
    def timer(self):
        pygame.time.set_timer(RESETEVENT, time)
        
    def restore (self):
        self.image = pygame.image.load("tanks/blue_tank.png")

        
    def hit(self):
        #Turn to red because player 2 was hit
        self.image = pygame.image.load("tanks/blue_hit.png")


 
#--Method to print text on screen --not used--
def message_to_screen(msg, color, xpos, ypos):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [xpos, ypos])


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
tankleftx_c = 0
tanklefty_c = 0

tankrightx = displaywidth/2 - 120
tankrighty = displayheight/2-10
tankrightx_c = 0
tankrighty_c = 0

player.rect.y = displayheight-30



# -------- Main Program Loop -----------
while not gameExit:
    
    # ----- Game Over -----    
    while gameOver == True:
        gameDisplay.fill(blue2)
        message_to_screen("Game over, press C to play again or Q to quit", red, displaywidth/2 - 200, displayheight/2)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameExit = True
                    gameOver = False
                if event.key == pygame.K_c:
                    gameExit = False
                    score = 0
                    score2 = 0
                    gameOver = False
    
    
    # ----- Event Processing  -----   
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            gameExit = True
            
        #Read keyboard events to move and shoot        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tankleftx_c -= block_size
                
            elif event.key == pygame.K_RIGHT:
                tankleftx_c += block_size
                
            elif event.key == pygame.K_UP:
                tanklefty_c -= block_size
                
            elif event.key == pygame.K_DOWN:
                tanklefty_c += block_size
                
            elif event.key == pygame.K_a:
                tankrightx_c -= block_size
                
            elif event.key == pygame.K_d:
                tankrightx_c += block_size
                
            elif event.key == pygame.K_w:
                tankrighty_c -= block_size
                
            elif event.key == pygame.K_s:
                tankrighty_c += block_size

            elif event.key == pygame.K_r:
                gameOver = True
            
            elif event.key == pygame.K_SPACE:
                # Fire a bullet if the user hits the Space Bar
                bullet = Bullet()
                # Set the bullet so it is where the player is
                bullet.rect.x = player.rect.x + 10
                bullet.rect.y = player.rect.y + 9
                # Add the bullet to the lists
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)
                
            elif event.key == pygame.K_TAB:
                # Fire a bullet if the user hits the Space Bar
                bullet2 = Bullet2()
                # Set the bullet so it is where the player is
                bullet2.rect.x = player2.rect.x + 85
                bullet2.rect.y = player2.rect.y + 9
                # Add the bullet to the lists
                all_sprites_list.add(bullet2)
                bullet2_list.add(bullet2)
                
        #Stop the tank if we have stopped pressing down        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                tankleftx_c = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                tanklefty_c = 0
                    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                tankrightx_c = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                tankrighty_c = 0
                
        #Reset the tanks back to their original color        
        if event.type == RESETEVENT:
                #print "Player 1 Hit"
                player.restore()
                pygame.time.set_timer(RESETEVENT, 0)
                
        if event.type == RESETEVENT2:
                #print "Player 2 Hit"
                player2.restore()
                pygame.time.set_timer(RESETEVENT2, 0)

    #Boundaries of each tank         
    if tankleftx + tankleftx_c > displaywidth - 40.5 or tankleftx + tankleftx_c < displaywidth/2:
        tankleftx_c = 0
    if tanklefty + tanklefty_c > displayheight - 20 or tanklefty + tanklefty_c < 0:
        tanklefty_c = 0
    if tankrightx + tankrightx_c > displaywidth/2 - 91 or tankrightx + tankrightx_c < displaywidth-850:
        tankrightx_c = 0
    if tankrighty + tankrighty_c > displayheight - 20 or tankrighty + tankrighty_c < displayheight-590:
        tankrighty_c = 0
        
    #Take the change and add it to the tank's position
    tankleftx += tankleftx_c
    tanklefty += tanklefty_c
    
    tankrightx += tankrightx_c
    tankrighty += tankrighty_c
    

    # --- Game logic
    
    # Call the update() method on all the sprites
    all_sprites_list.update()

    # Calculate collisions for bullets from player 1
    for bullet in bullet_list:
        
        # If player 2 is hit, remove the bullet, add to the player 1 score and turn the player 2 tank red
        if player2.rect.x + 80 > bullet.rect.x > player2.rect.x - 20 and player2.rect.y + 50 > bullet.rect.y > player2.rect.y - 20:
            player2.hit()
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
        elif bullet.rect.x < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
                
            """Use the code below to penalize tank 1 for missing after shooting"""
            #  if score <= 8.5 and score2 != -15:
            #      score -= 0.1
               #print ("Tank 1 missed!")

            
          
    # Calculate collisions for bullets from player 2
    for bullet2 in bullet2_list:
        
        # If the player 1 is hit, remove the bullet and add to the player 2 score   
        if player.rect.x + 20 > bullet2.rect.x > player.rect.x - 10 and player.rect.y + 50 > bullet2.rect.y > player.rect.y - 20:
            player.hit()
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
        elif bullet2.rect.x > displaywidth + 10:
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
    pygame.draw.rect(gameDisplay, black, [displaywidth/2,displayheight-600 , 5, displayheight])

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


