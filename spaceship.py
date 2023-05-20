import pygame as py
from constants import HEIGHT_SCREEN, WIDTH_SCREEN
from random import randint
from numpy import cos, sin, deg2rad
from missile import Missile

class Spaceship():
    """
    Class of the spaceship that the player controls.

    float x,y : position of the spaceship
    int angle : angle of the spaceship in degrees
    list[float] mvtVector : vector of the movement
    list[py.Surface] texture : list of textures of the spaceship
    bool boost : state of the booster
    py.Rect rect : current rect
    py.Rect lastRect : rect of the last frame
    py.Surface img : current image
    int life : lifes remaining
    """
    x = randint(20,WIDTH_SCREEN-20)
    y = randint(20,HEIGHT_SCREEN//4)
    angle = 0
    mvtVector = [0,0]
    bouncing = False
    texture = [py.transform.scale(py.image.load("spaceship.png"),(24,21))]
    texture.append(py.transform.scale(py.image.load("spaceship_booster.png"),(24,21)))
    boost = False
    rect = texture[0].get_rect()
    lastRect = None
    img = texture[0]
    life = 3


    def __init__(self, screen:py.Surface):
        """
        Create a new Spaceship object.

        py.Surface screen : screen of the game
        py.mixer.Sound Colision : sounds of colisions
        """
        self.screen = screen
        self.Colision = [py.mixer.Sound("Colision_1.wav"),py.mixer.Sound("Colision_2.wav")]

    
    def getRect(self)->py.Rect:
        """
        Return current rect.
        """
        return self.rect
    
    def getPos(self)->tuple[int]:
        """
        Return current rounded position.
        """
        return (round(self.x)-24,round(self.y)-21)
    
    def updateRect(self):
        """
        Update the current rect according to the new position.
        """
        img = self.texture[self.boost]
        self.rect = self.img.get_rect(center=img.get_rect(center=(round(self.x),round(self.y))).center)

    def draw(self):
        """
        Draw the current texture on the screen according to the
        acutal rect and the booster.
        """
        img = self.texture[self.boost]
        self.img = py.transform.rotate(img,self.angle)
        self.rect = self.img.get_rect(center=img.get_rect(center=(round(self.x),round(self.y))).center)
        self.screen.blit(self.img,self.rect)
    
    def drawBackground(self,background):
        """
        Draw the image of the background on the last postion of
        the player.
        
        py.Surface background : image of the background
        """
        if self.lastRect:
            img = background.subsurface(self.lastRect)
            self.screen.blit(img,self.lastRect)
    
    def start_booster(self):
        """
        Active booster.
        """
        self.boost = True
    
    def stop_booster(self):
        """
        Stop booster.
        """
        self.boost = False

    def turnLeft(self):
        """
        Turn the spaceship on the left
        """
        self.angle += 4
        if self.angle > 360:
            self.angle -= 360

    def turnRight(self):
        """
        Turn the spaceship on the right
        """
        self.angle -= 4
        if self.angle < 0:
            self.angle += 360

    def correctVector(self):
        """
        Normalize the vector of movement (mvtVector) if its
        norme is higher than the speed limit."""
        MAX_SPEED = 2.5
        s = abs(self.mvtVector[0]) + abs(self.mvtVector[1])
        if s > MAX_SPEED :
            #Normalize vector if greater than speed limit
            self.mvtVector[0] = self.mvtVector[0] / s * MAX_SPEED
            self.mvtVector[1] = self.mvtVector[1] / s * MAX_SPEED

    def move(self):
        """
        Move the spaceship.
        If booster is active, raise the movement vector according to
        the angle.
        Trigger the correctVector method.
        """
        ACCELERATION = 0.05

        if self.boost:
            #Create vector for movement
            fx = cos(deg2rad(self.angle)) * ACCELERATION
            fy = sin(-deg2rad(self.angle)) * ACCELERATION
            #Add them up
            self.mvtVector[0] += fx
            self.mvtVector[1] += fy
        
        self.correctVector()
        self.x += self.mvtVector[0]
        self.y += self.mvtVector[1]
        self.lastRect = self.rect
        self.updateRect()

    def shoot(self,missileList:list[Missile]):
        """
        Create and add to the missileList a new missile shot by
        the spaceship.
        If there are already 4 missiles nothing is done.
        
        list[Missile] missileList : list of all missiles
        """
        count = 0
        for mis in missileList:
            if mis.fromPlayer():
                count += 1
        if count < 4:
            missileList.append(Missile(self.angle,False,self.x,self.y,self.screen))
        
    def death(self):
        if self.life == 0:
            py.mixer.Sound("death.wav")

    def bounce(self, vect:list[int]):
        """
        The spaceship bounce on a border and lower its speed.
        Trigger updateRect method.
        
        list[int] vect : normal vector of the border the supership bounced on
        """
        self.bouncing = True
        self.x -= self.mvtVector[0]
        self.y -= self.mvtVector[1]
        self.x += vect[0]
        self.y += vect[1]
        self.updateRect()
        if vect[1] == 0:
            self.mvtVector[0] /= -2
        else:
            self.mvtVector[1] /= -2
        
