import pygame
import cv2
screen = pygame.display.set_mode((640, 400))
running = 1
import sys

import fancyFunction as ro
cap = cv2.VideoCapture(1);
while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0
    (grabbed, frame) = cap.read()
    s,t = ro.getPosition(frame)
    pygame.draw.circle(screen, (0,0,0), s, 100, 5)
    pygame.display.update()
    screen.fill((255, 255,255))
    pygame.display.flip()