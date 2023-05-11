import pygame as py
from random import randint
from numpy import log

class Droid:
    """
    Create a droid.
    It is a passive slow ennemy moving around the center.
    """

    def __init__(self,x:int,y:int,wave:int,rotation:bool,screen:py.Surface):
        self.x = x
        self.y = y
        self.posX = x
        self.posY = y
        if rotation:
            self.step = 3
            self.objectiv = randint(9,396)
        else:
            self.step = 2
            self.objectiv = randint(852,1239)
        self.speed = log(wave+200)
        self.rot = rotation
        self.texture = [py.image.load("droid1.png"),py.image.load("droid2.png")]
        for i in range(len(self.texture)):
            self.texture[i] = py.transform.scale(self.texture[i],(32,32))
        self.texturePos = 0
        self.rect = self.texture[0].get_rect(topleft=(x,y))
        self.lastRect = None
        self.transformTime = randint(2000,2500)
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
        if self.lastRect:
            img = background.subsurface(self.lastRect)
            self.screen.blit(img, self.lastRect)

    def objectivReached(self)->bool:
        if self.rot:
            if self.step == 0 and self.posY <= self.objectiv:
                self.objectiv = randint(852,1239)
                return True
            elif self.step == 1 and self.posX >= self.objectiv:
                self.objectiv = randint(478,679)
                return True
            elif self.step == 2 and self.posY >= self.objectiv:
                self.objectiv = randint(9,396)
                return True
            elif self.step == 3 and self.posX <= self.objectiv:
                self.objectiv = randint(9,210)
                return True
        else:
            if self.step == 0 and self.posX <= self.objectiv:
                self.objectiv = randint(478,679)
                return True
            elif self.step == 3 and self.posY >= self.objectiv:
                self.objectiv = randint(852,1239)
                return True
            elif self.step == 2 and self.posX >= self.objectiv:
                self.objectiv = randint(9,210)
                return True
            elif self.step == 1 and self.posY <= self.objectiv:
                self.objectiv = randint(9,396)
                return True
        return False
    
    def move(self, missileList, foesList, playerPos):
        if self.objectivReached():
            if self.rot:
                self.step += 1
            else:
                self.step -= 1
            if self.step > 3:
                self.step = 0
            elif self.step < 0:
                self.step = 3
        
        #move to next step
        self.lastRect = self.rect
        if self.rot:
            if self.step%2 == 1:
                self.x -= (self.step-2) * 0.1 * self.speed
            else:
                self.y += (self.step-1) * 0.1 * self.speed
        elif self.step%2 == 0:
            self.x += (self.step-1) * 0.1 * self.speed
        else:
            self.y += (self.step-2) * 0.1 * self.speed
        
        self.posX = round(self.x)
        self.posY = round(self.y)
        self.rect = self.texture[0].get_rect(topleft=(self.posX,self.posY))

    def bounce(self, axis):
        pass