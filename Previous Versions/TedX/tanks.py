#
# tanks.py
#
#   This file implements the display of the tanks in ARBattles!
#   Yippie!
#
#   The tank images are assumed to be square.  Currently using 70 pixel images.
#   Over time this could be converted to deal with non-square images.
#   It is assumed that it is "pleasing" to have the image rotate around it's center.
#

import os,pygame

#
# Tank
#     .pos = a rectangle where the tank is, or None if the tank hasn't yet been drawn
#
class Tank:

    def __init__(self,color):
        self.origImage = self._tankLoad(color)
        self.width = self.origImage.get_width()
        self.height = self.origImage.get_height()
        self.pos = pygame.Rect((0,0),(self.width,self.height))
        self.rotation = 0
        self.image = self.origImage

    def move(self,pos,rotation):
        self.pos.center = pos
        self._rotate(rotation)

    def _rotate(self, angle):
        if angle:
            orig_rect = self.origImage.get_rect()
            rot_image = pygame.transform.rotate(self.origImage, angle)
            rot_rect = orig_rect.copy()
            rot_rect.center = rot_image.get_rect().center
            self.image = rot_image.subsurface(rot_rect).copy()

    def _tankLoad(self,color):
        main_dir = os.path.split(os.path.abspath(__file__))[0]
        #path = os.path.join(main_dir, 'Media', color + "200.png")
        path = os.path.join(main_dir, 'Media', color + "200.gif")
        return pygame.image.load(path).convert_alpha()

    def draw(self,screen):
        screen.blit(self.image,self.pos)
        pygame.draw.circle(screen,(255,255,255),self.pos.center,50)
