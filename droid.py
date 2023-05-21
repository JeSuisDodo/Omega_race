import pygame as py
from random import randint
from numpy import log
from mothership import MotherShip

class Droid:
    """
    Create a droid.
    It is a passive slow ennemy moving around the center.
    After a while, it starts transforming into a mothership

    list[py.Surface] texture : all the texture of the ennemy
    py.Surface motherTexture : texture of the mothership
    int transfromTime : time left in gameloops before it completes
        its transformation
    int texturePos : the current texture it displays
    """
    texture = [py.image.load("droid1.png"),py.image.load("droid2.png")]
    for i in range(len(texture)):
        texture[i] = py.transform.scale(texture[i],(32,32))
    motherTexture = [py.image.load("mothership1.png"),py.image.load("mothership2.png")]
    for i in range(len(motherTexture)):
        motherTexture[i] = py.transform.scale(motherTexture[i],(32,32))
    transformTime = 500
    texturePos = 0

    def __init__(self,x:float,y:float,wave:int,rotation:bool,screen:py.Surface):
        """
        float x,y : real position of the ennemy
        int posX, posY : position of the ennemy after a round
        int step : where the ennemy is going
            if 0 -> top left
            if 1 -> top right
            if 2 -> bottom right
            if 3 -> bottom left
        int objectiv : the x or y position the ennemy must reach
            to complete the 'step'
        int wave : current wave
        float speed : speed of the ennemy based on the wave
        bool rot : tell if the ennemy is moving clock-wise
        py.Rect rect : current rect object of the ennemy
        py.Rect lastRect : rect object of the last position
        py.Surface screen : the screen of the game
        int timeBeforeTransform : time left in gameloops before the
            ennemy transform
        """
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
        self.wave = wave
        self.speed = log(wave)
        self.rot = rotation
        self.rect = self.texture[0].get_rect(topleft=(x,y))
        self.lastRect = None
        self.screen = screen
        self.timeBeforeTransform = randint(1000,2500)
    
    def getRect(self)->py.Rect:
        """
        Return the current rect.
        """
        return self.rect
    
    def getCo(self)->tuple[int]:
        """
        Return a tuple of rounded position.
        """
        return (self.posX,self.posY)
    
    def draw(self):
        """
        Draw the current texture on the screen according to the current rect.
        If it is transforming then it shows half the time the texture of the
        mothership.
        """
        if self.timeBeforeTransform == 0 and self.transformTime%40<20:
            self.screen.blit(self.motherTexture[self.texturePos//50],self.rect)
        else:
            self.screen.blit(self.texture[self.texturePos//50],self.rect)
        
        self.texturePos += 1
        if self.texturePos >= 100:
            self.texturePos = 0
    
    def drawBackground(self, background:py.Surface):
        """
        Draw the image of the background on the last postion of
        the ennemy.
        
        py.Surface background : the image of the background
        """
        if self.lastRect:
            #Take the portion of the background where the ennemy was
            img = background.subsurface(self.lastRect)
            self.screen.blit(img, self.lastRect)

    def objectivReached(self)->bool:
        """
        Return True if the ennemy reached the 'step', False else.
        If it has reached the step. Create a new one.
        """
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
    
    def move(self, foesList:list):
        """
        Move the ennemy if it is not during the transformation into a
        mothership.
        Then, update the rect and the rounded position.

        list foesList : the list of all the ennemies and the mines
        """
        #Check for transformation
        if self.transformTime == 0:
            #Delete the object and add a new mothership at the same position
            foesList.append(MotherShip(self.posX,self.posY,self.wave,self.rot,self.screen))
            foesList.remove(self)
            return
        elif self.timeBeforeTransform == 0 and self.transformTime > 0:
            self.transformTime -= 1
            return
        
        #Update time for transformation
        self.timeBeforeTransform -= 1
        #Check the objectiv
        if self.objectivReached():
            if self.rot:
                self.step += 1
            else:
                self.step -= 1
            if self.step > 3:
                self.step = 0
            elif self.step < 0:
                self.step = 3
        
        #Remember last rect
        self.lastRect = self.rect
        #Move to next step
        if self.rot:
            if self.step%2 == 1:
                self.x -= (self.step-2) * 0.1 * self.speed
            else:
                self.y += (self.step-1) * 0.1 * self.speed
        elif self.step%2 == 0:
            self.x += (self.step-1) * 0.1 * self.speed
        else:
            self.y += (self.step-2) * 0.1 * self.speed
        
        #Update rounded positiion and rect
        self.posX = round(self.x)
        self.posY = round(self.y)
        self.rect = self.texture[0].get_rect(topleft=(self.posX,self.posY))