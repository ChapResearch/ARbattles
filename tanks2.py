import pygame
import cv2
screen = pygame.display.set_mode((640, 500))
running = 1
import time
import sys

import RecognizerFunciton as ro
cap = cv2.VideoCapture(0);
bulletsPos = [(0,0)];
pressed = False;
lifespan = 200
while running:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pressed = True
                lifespan = 20



    (grabbed, frame) = cap.read()
    try:
        XB,XS,YB,YS = ro.getPosition(frame)
        #print XB["Triangle"], YB["Triangle"]
        pygame.draw.circle(screen, (0,0,0), (XB["Triangle"],YB["Triangle"]), 20, 5)
        pygame.draw.circle(screen, (0,0,0), (XS["Triangle"],YS["Triangle"]), 20, 5)
        pygame.draw.circle(screen, (0,0,0), (XB["Quadrilateral"],YB["Quadrilateral"]), 20, 5)
        pygame.draw.circle(screen, (0,0,0), (XS["Quadrilateral"],YS["Quadrilateral"]), 20, 5)
        #print(pressed)
        if pressed:
            print(pressed)
            bulletsPos.append(bulletsPos, [((XS["Triangle"] - (XB["Triangle"]-XS["Triangle"]),YS["Triangle"] - (YB["Triangle"]-YS["Triangle"])))])
            pressed = False

        print bulletsPos
        if lifespan >=0:
            for i in range[0,bulletsPos.len()/2-1]:
                pygame.draw.circle(screen, (0,255,0), (bulletsPos[i],bulletsPos[i+1]), 20, 5)
                lifespan = lifespan-1;

    except:
        print"err"
    pygame.display.update()
    screen.fill((255,255,255))
