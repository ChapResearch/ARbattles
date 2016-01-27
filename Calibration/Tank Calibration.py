import pygame
import time


pygame.init()

blue = (73, 109, 173)
white = (255, 255, 255)

gameExit = False
clock = pygame.time.Clock()

# Set the height and width of the display
displaywidth = 600
displayheight = 400

gameDisplay = pygame.display.set_mode([displaywidth, displayheight],pygame.FULLSCREEN)
pygame.display.set_caption('ARbattles Calibrations')


while not gameExit:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                gameExit = True
                
    gameDisplay.fill(white)
    pygame.draw.rect(gameDisplay, blue ,[0,0,displaywidth/2,displayheight/2])
    pygame.draw.rect(gameDisplay, blue ,[displaywidth/2+60,displayheight/2+60,(displaywidth/2),(displayheight/2)])
    
    """
    pygame.draw.rect(gameDisplay, blue ,[0,0,50,50])
    pygame.draw.rect(gameDisplay, blue ,[displaywidth - 50, displayheight - 50, 50, 50])
    pygame.draw.rect(gameDisplay, blue ,[displaywidth - 50,0,50,50])
    pygame.draw.rect(gameDisplay, blue ,[0,displayheight - 50,50,50])
    """
    pygame.display.update()
  
    clock.tick(20)
    
pygame.quit()
quit()



