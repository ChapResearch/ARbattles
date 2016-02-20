import pygame

white = (255,255,255)
red = (206, 16, 98)


width = 750
height = 500
#aDisplay = pygame.display.set_mode([width, height])

def calibrationSquares (gameDisplay, displaywidth, displayheight):
    gameDisplay.fill((255,255,255))
    pygame.draw.rect(gameDisplay, red, [0, 0, displaywidth/4 + 25, displayheight/4 + 40])
    pygame.draw.rect(gameDisplay, red,[displaywidth - 140, displayheight - 140, (displaywidth/4), (displayheight/4 + 40)])

"""
gameExit = False
while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                gameExit = True
        else:
            calibrationSquares(gameDisplay,displaywidth, displayheight)
pygame.quit()
"""