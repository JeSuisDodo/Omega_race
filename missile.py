import pygame as py
from numpy import cos, sin, deg2rad
import constants

class Missile:
    """
    Create a missile object
    """

    def __init__(self, angle:int, harmPlayer:bool, x:int, y:int,screen):
        self.x = x
        self.y = y
        self.posX = x
        self.posY = y
        self.texture = py.transform.rotate(py.image.load("missile.png"),angle)
        self.rect = self.texture.get_rect(center=self.texture.get_rect(topleft=(x,y)).center)
        self.lastRect = None
        self.angle = angle
        self.canHarmPlayer = harmPlayer
        self.screen = screen

    def type(self):
        return Missile
    
    def getRect(self):
        return self.rect

    def getHitbox(self):
        """
        Return the top-left and bottom right coordinates of
        the rect made by the missile
        """
        x1, y1 = self.posX, self.posY
        x2 = self.posX+round(13*cos(deg2rad(self.angle)))
        y2 = self.posY+round(13*sin(-deg2rad(self.angle)))
        
        if x2 < x1:
            return (x2, y2, x1, y1)
        return (x1, y1, x2, y2)
    
    def fromPlayer(self):
        return not(self.canHarmPlayer)

    def move(self):
        self.lastRect = self.texture.get_rect(center=self.texture.get_rect(topleft=(self.posX,self.posY)).center)
        self.x += 3.5 * cos(deg2rad(self.angle))
        self.y += 3.5 * sin(-deg2rad(self.angle))
        self.posX = round(self.x)
        self.posY = round(self.y)
        self.rect = self.texture.get_rect(center=self.texture.get_rect(topleft=(self.posX,self.posY)).center)
    
    def drawBackground(self,background):
        if self.lastRect:
            img = background.subsurface(self.lastRect)
            self.screen.blit(img,self.lastRect)

    def draw(self):
        self.screen.blit(self.texture,self.rect)
        """
        if self.canHarmPlayer:
            color = constants.RED
        else:
            color = constants.WHITE
        print("D (",self.posX,self.posY,") à (",self.posX+round(13*cos(deg2rad(self.angle))),
             self.posY+round(13*sin(-deg2rad(self.angle))),")")
        py.draw.rect(self.screen,color,self.getPosRect(),1)
        #py.draw.line(self.screen, color,
        #    (self.posX,self.posY),
        #    (self.posX+round(13*cos(deg2rad(self.angle))),
        #     self.posY+round(13*sin(-deg2rad(self.angle)))),3)
        """
    
    def die(self, background):
        img = background.subsurface(self.rect)
        img2 = background.subsurface(self.lastRect)
        self.screen.blit(img,self.rect)
        self.screen.blit(img2,self.lastRect)