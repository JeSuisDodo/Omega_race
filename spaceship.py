import pygame as py
from constants import *
from random import randint
from numpy import cos, sin, deg2rad
import border
import missile

class Spaceship():
    """
    Class of the spaceship that the player control
    """

    def __init__(self, screen) -> None:
        """
        Create a new Spaceship object
        """
        self.x = randint(20,WIDTH_SCREEN-20)
        self.y = randint(20,HEIGHT_SCREEN//4)
        self.angle = 0
        self.mvtVector = [0,0]
        self.bouncing = None
        self.screen = screen
        self.texture = [py.transform.scale(py.image.load("spaceship.png"),(24,21))]
        self.texture.append(py.transform.scale(py.image.load("spaceship_booster.png"),(24,21)))
        self.boost = False
        self.rect = self.texture[0].get_rect()
        self.life = 3
        self.Colision = [py.mixer.Sound("Colision_1.wav"),
                         py.mixer.Sound("Colision_2.wav")]
        self.score = 0
    
    def type(self):
        return Spaceship
    
    def getRect(self):
        return self.rect
    
    def getPos(self):
        return (round(self.x),round(self.y))

    def draw(self):
        img = self.texture[self.boost]
        R_img = py.transform.rotate(img,self.angle)
        R_rect = R_img.get_rect(center=img.get_rect(center=(round(self.x),round(self.y))).center)
        self.rect = R_rect
        self.screen.blit(R_img,R_rect)
    
    def drawBackground(self,background):
        img = background.subsurface(self.rect)
        self.screen.blit(img,self.rect)
    
    def booster(self):
        self.boost = True
        # self.speed += 0.2
        # if self.speed > self.maxSpeed:
        #     self.speed = self.maxSpeed
    
    def stop_booster(self):
        self.boost = False

    def turnLeft(self):
        self.angle += 4
        if self.angle > 360:
            self.angle -= 360

    def turnRight(self):
        self.angle -= 4
        if self.angle < 0:
            self.angle += 360

    def correctVector(self):
        MAX_SPEED = 2.5
        s = abs(self.mvtVector[0]) + abs(self.mvtVector[1])
        if s > MAX_SPEED :
            #Normalize vector if greater than speed limit
            #d = max(abs(self.mvtVector[0]),abs(self.mvtVector[1]))
            self.mvtVector[0] = self.mvtVector[0] / s * MAX_SPEED
            self.mvtVector[1] = self.mvtVector[1] / s * MAX_SPEED

    def bouncingCooldown(self):
        if self.bouncing:
            self.bouncing[0] -= 1
            if self.bouncing[0] <= 0:
                self.bouncing = None

    def move(self):
        ACCELERATION_MODIFIER = 0.1
        
        if self.bouncing == [5,'x']:
            self.mvtVector[1] /= -2
            
        elif self.bouncing == [5,'y']:
            self.mvtVector[0] /= -2

        elif self.boost and not self.bouncing:
            #Create vector for movement
            fx = cos(deg2rad(self.angle)) * ACCELERATION_MODIFIER
            fy = sin(-deg2rad(self.angle)) * ACCELERATION_MODIFIER
            #Add them up
            self.mvtVector[0] += fx
            self.mvtVector[1] += fy
        
        self.bouncingCooldown()
        self.correctVector()
        self.x += self.mvtVector[0]
        self.y += self.mvtVector[1]

    def shoot(self,missileList):
        if len(missileList) < 4:
            missileList.append(missile.Missile(self.angle,
                                               False,self.x,self.y,self.screen))
        

    def death(self):
        if self.life == 0:
            py.mixer.Sound("death.wav")
    
    def resetBounce(self):
        self.bouncing = None

    def bounce(self, axis):
        if not self.bouncing:
            self.bouncing = [5,axis]
            py.mixer.Sound.play(self.Colision[randint(0,1)])