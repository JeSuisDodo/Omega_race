import pygame as py
from numpy import cos, sin, deg2rad

class Missile:
    """
    Class of the missile.
    It moves forward in the a given angle until
    hurting something.
    """

    def __init__(self, angle:int, harmPlayer:bool, x:float, y:float,screen:py.Surface):
        """
        Create a new missile object.

        int angle : angle in degrees
        bool canHarmPlayer : can the missile hurt the player
        float x,y : real position of the missile
        int posX, posY : rounded position
        py.Surface texture : texture of the missile with respect of the angle
        py.Rect rect : rect object describing the missile
        py.Surface screen : screen of the game
        """
        self.x = x
        self.y = y
        self.posX = x
        self.posY = y
        self.texture = py.transform.rotate(py.image.load("missile.png"),angle)
        self.rect = self.texture.get_rect(center=self.texture.get_rect(topleft=(x,y)).center)
        self.lastRect = None
        self.angle = angle
        self.canHarmPlayer = harmPlayer
        if harmPlayer:
            w, h = self.texture.get_size()
            for i in range(w):
                for j in range(h):
                    self.texture.set_at((i,j),py.Color((255,100,100)))
        self.screen = screen
    
    def getHitbox(self)->tuple[int]:
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
    
    def fromPlayer(self)->bool:
        """
        Return True if the player shot the missile.
        """
        return not(self.canHarmPlayer)

    def move(self):
        """
        Move the missile according to the angle.
        Then update rounded position and rect.
        """
        self.lastRect = self.texture.get_rect(center=self.texture.get_rect(topleft=(self.posX,self.posY)).center)
        self.x += 3.5 * cos(deg2rad(self.angle))
        self.y += 3.5 * sin(-deg2rad(self.angle))
        self.posX = round(self.x)
        self.posY = round(self.y)
        self.rect = self.texture.get_rect(center=self.texture.get_rect(topleft=(self.posX,self.posY)).center)
    
    def drawBackground(self,background:py.Surface):
        """
        Draw the image of the background on the last postion of
        the missile.

        py.Surface background : image of the background
        """
        if self.lastRect:
            img = background.subsurface(self.lastRect)
            self.screen.blit(img,self.lastRect)

    def draw(self):
        """
        Draw the missile on the screen.
        """
        self.screen.blit(self.texture,self.rect)
    
    def die(self, background:py.Surface):
        """
        Erase the missile from the screen and draw the background.

        py.Surface background : background's texture
        """
        img = background.subsurface(self.rect)
        img2 = background.subsurface(self.lastRect)
        self.screen.blit(img,self.rect)
        self.screen.blit(img2,self.lastRect)