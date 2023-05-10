import pygame as py
from random import randint

class Droid:
    """
    Create a droid
    """

    def __init__(self,x,y,screen):
        self.x = x
        self.y = y
        self.texture = [py.image.load("droid1.png"),py.image.load("droid2.png")]
        for i in range(len(self.texture)):
            self.texture[i] = py.transform.scale(self.texture[i],(32,32))
        self.texturePos = 0
        self.rect = self.texture[0].get_rect(topleft=(self.x,self.y))
        self.transformTime = randint(1000,1500)
        self.screen = screen
    
    def type(self):
        return Droid
    
    def getRect(self):
        return self.rect
    
    def draw(self):
        self.screen.blit(self.texture[self.texturePos//50],self.rect)
        self.texturePos += 1
        if self.texturePos >= 100:
            self.texturePos = 0
    
    def drawBackground(self, background):
        img = background.subsurface(self.rect)
        self.screen.blit(img, self.rect)
    
    def move(self, missileList, foesList, playerPos):
        pass

    def bounce(self, axis):
        pass