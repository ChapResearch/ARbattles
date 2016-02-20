import os, pygame
import datetime
import time
from tanks import Tank

pygame.init()
screen = pygame.display.set_mode((640, 480))

tank1 = Tank("blue")
tank2 = Tank("green")

def loadField(name):
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    path = os.path.join(main_dir, 'Media', name)
    return pygame.image.load(path).convert()
    
def main():
    WHITE = (255, 255, 255)

    clock = pygame.time.Clock()

    background = loadField("field640x480.png")

    screen.blit(background, (0, 0))
    pygame.display.update()

    tank1Pos = (100,100)
    tank2Pos = (300,300)

    tank1Rotation = 0
    tank2Rotation = 0

    #
    # the move point is the CENTER of the tank
    #
    tank1.move(tank1Pos,tank1Rotation)
    tank2.move(tank2Pos,tank2Rotation)
    
    screen.blit(tank1.image,tank1.pos,tank1.pos)
    screen.blit(tank2.image,tank2.pos,tank2.pos)

    pygame.display.update()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tank1Rotation += 10
                    tank1Pos = (tank1Pos[0]+1,tank1Pos[1]-1)
                    tank2Rotation -= 10
                    tank2Pos = (tank2Pos[0]-1,tank2Pos[1]+1)
                if event.key == pygame.K_RIGHT:
                    tank1Rotation -= 10
                    tank1Pos = (tank1Pos[0]-1,tank1Pos[1]+1)
                    tank2Rotation += 10
                    tank2Pos = (tank2Pos[0]+1,tank2Pos[1]-1)

        # this can be replaced with other erasing routines, but this is fast
        screen.blit(background,tank1.pos,tank1.pos)
        screen.blit(background,tank2.pos,tank2.pos)

        # no movement (just rotation) can be done with:
        #   tank1.move(tank1.pos.center,tank1Rotation)
        #
        tank1.move(tank1Pos,tank1Rotation)
        tank2.move(tank2Pos,tank2Rotation)

        tank1.draw(screen)
        tank2.draw(screen)

        pygame.display.update()

        clock.tick(5)

main()
pygame.quit()
