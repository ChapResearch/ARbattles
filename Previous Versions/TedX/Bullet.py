import pygame
import math

#-----Bullet Classes-----

##Bullet 1 class
    #Takes: Bullet_sizex, bulletsize_y, color, rotationRobot1
class Bullet (pygame.sprite.Sprite):
    """ This class represents the missile for the Triangle Tank. """
    def __init__(self, bullet_sizex, bullet_sizey, color):
        # Call the parent class (Sprite) constructor
        super(Bullet, self).__init__()

        self.image = pygame.Surface([bullet_sizex, bullet_sizey])
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.x += (bullet_sizex * math.cos(rotationRobot1)) * 5
        self.rect.y += (bullet_sizey * math.sin(rotationRobot1)) * -5

##Bullet 2 class
    #Takes: Bullet_sizex, bulletsize_y, color2, rotationRobot2
class Bullet2 (pygame.sprite.Sprite):
    """ This class represents the missile for the Square Tank """
    def __init__(self, bullet_sizex, bullet_sizey, color2):
        # Call the parent class (Sprite) constructor
        super(Bullet2, self).__init__()

        self.image = pygame.Surface([bullet_sizex, bullet_sizey])
        self.image.fill(color2)
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.x += (bullet_sizex * math.cos(rotationRobot2))* 5
        self.rect.y += (bullet_sizey * math.sin(rotationRobot2))* -5

####Bullet Collisions
    # Calculate collisions for bullets from player 1
        #Needs: Bullet list, center robot 2, distance 2, circle2 timer, all_sprites_list, score, score2
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



####Bullet 2 Collisions
            #Needs: Bullet list 2, center robot 1, distance 1, circle timer, all_sprites_list, score, score2

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
