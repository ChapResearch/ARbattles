import pygame
import CalibrationFunction

pygame.init()

red = (206, 16, 98)
white = (255, 255, 255)


gameExit = False
clock = pygame.time.Clock()

# Set the height and width of the display
displaywidth = 750
displayheight = 500


gameDisplay = pygame.display.set_mode([displaywidth, displayheight])
pygame.display.set_caption('ARbattles Calibrations')


while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                gameExit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                gameExit = True

            if event.key == pygame.K_a:
                gameDisplay = pygame.display.set_mode([displaywidth, displayheight])

            if event.key == pygame.K_f:
                gameDisplay = pygame.display.set_mode([displaywidth, displayheight], pygame.NOFRAME)

            if event.key == pygame.K_w:
                gameDisplay = pygame.display.set_mode([displaywidth, displayheight])

    CalibrationFunction.calibrationSquares(gameDisplay, displaywidth, displayheight)
    pygame.display.update()
    
pygame.quit()
quit()



