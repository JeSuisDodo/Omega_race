import pygame as py
import constants
import spaceship

class border():
    """
    Create a border object
    """

    def __init__(self, x:int, y:int, h:int, l:int, axis:str, type:str, screen) -> None:
        """(x,y) coordinates of the start of the border
        \nh height of the border
        \nl length of the border
        \naxis 'x' or 'y' the player can come from to collide with the border
        \nscreen is the screen
        """
        self.x = x
        self.y = y
        self.h = h
        self.l = l
        self.line = (x,y,x+l,y+h)
        self.axis = axis
        if axis == 'x':
            self.surfAlpha = py.Surface((self.l,3), py.SRCALPHA)
        else :
            self.surfAlpha = py.Surface((3,self.h),py.SRCALPHA)
        self.outer = (type == "Outer")
        self.screen = screen
        self.alpha = 0
    
    def getAxis(self):
        return self.axis
    
    def isOuter(self):
        return self.outer

    def decreaseAlpha(self,n:int):
        self.alpha -= n
        if self.alpha < 0:
            self.alpha = 0

    def setAlpha(self,n:int):
        self.alpha = n

    def drawAlpha(self, color):
        self.surfAlpha.fill((color[0],color[1],color[2],self.alpha))
        self.screen.blit(self.surfAlpha,(self.x,self.y))

    def draw(self,color):
        py.draw.line(self.screen, color, (self.x,self.y), (self.x+self.l,self.y+self.h),3)

    def collides_with_rect(self, obj):
        if obj.getRect().clipline(self.line):
            return True
        return False
    
    def collides_with_line(self,obj):
        x1, y1, x2, y2 = obj.getHitbox()
        if self.axis == 'x':
            return (self.x < x2 and (self.x+self.l) > x1 and
                     ((y1 <= self.y <= y2) or (y2 <= self.y <= y1)))
        return (self.y < y2 and (self.y+self.h) > y1 and
                ((x1 <= self.x <= x2) or (x2 <= self.x <= x1)))

