import pygame as py

class Border():
    """
    Class of the border.
    They are straight lines that nothing can go trough.
    Player and ennemies bounce on it and missiles are destroyed.

    int alpha : transparancy level for outer borders
    """
    alpha = 0

    def __init__(self, x:int, y:int, h:int, w:int, vectNormal:tuple, type:str, screen) -> None:
        """
        Create a new border object.

        int x,y : top left of the border
        int h : height of the border
        int w : width of the border
        tuple[int] line : line object format for pygame colliding tests
        py.Surface surfAlpha : surface with transparancy mathcing the border texture
        bool outer : is the border in the inner or outer rectangle. True if outer.
        py.Surface screen : screen of the game
        """
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.line = (x,y,x+w,y+h)
        self.vectNormal = vectNormal
        if vectNormal[0] == 0:
            self.surfAlpha = py.Surface((w,3), py.SRCALPHA)
        else :
            self.surfAlpha = py.Surface((3,h),py.SRCALPHA)
        self.outer = (type == "Outer")
        self.screen = screen
    
    def getNormalVector(self)->list[int]:
        """
        Return the normal vector.
        """
        return self.vectNormal
    
    def isOuter(self)->bool:
        """
        Return True if the border is in the outer rectangle.
        """
        return self.outer
    
    def getRect(self)->py.Rect:
        """
        Return a rect object describing the border.
        """
        if self.vectNormal[0] == 0:
            return py.Rect(self.x,self.y,self.w,3)
        return py.Rect(self.x,self.y,3,self.h)

    def decreaseAlpha(self,n:int):
        """
        Lower alpha value by n a parameter.

        int n : number to lower the alpha value
        """
        self.alpha -= n
        if self.alpha < 0:
            self.alpha = 0

    def setAlpha(self,n:int):
        """
        Set the current alpha value to n a parameter.
        
        int n : new value of the alpha transparancy
        """
        self.alpha = n

    def drawAlpha(self, color:tuple):
        """
        Draw the border with respect of the transparancy level.

        tuple color : color in pygame format
        """
        self.surfAlpha.fill((color[0],color[1],color[2],self.alpha))
        self.screen.blit(self.surfAlpha,(self.x,self.y))

    def draw(self,color:tuple):
        """
        Draw the border on the screen.

        tuple color : color in pygame format
        """
        py.draw.line(self.screen, color, (self.x,self.y), (self.x+self.w,self.y+self.h),3)

    def drawBackground(self, background:py.Surface):
        """
        Draw the background on the position of the border.

        pu.Surface background : image of the background
        """
        if self.alpha > 0:
            rect = self.getRect()
            img = background.subsurface(rect)
            self.screen.blit(img,rect)

    def collides_with_rect(self, obj)->bool:
        """
        Return True if the object obj in parameter touch the border.
        The object obj must have a getRect method.

        obj : test object which can be any ennemy
        """
        return obj.getRect().clipline(self.line)
    
    def collides_with_line(self,obj)->bool:
        """
        Return True if the object obj in parameter touch the border.
        The object obj must be in a line format with a getHitbox method.
        
        obj : test object, a missile"""
        x1, y1, x2, y2 = obj.getHitbox()
        if self.vectNormal[0] == 0:
            return (self.x < x2 and (self.x+self.w) > x1 and
                     ((y1 <= self.y <= y2) or (y2 <= self.y <= y1)))
        return (self.y < y2 and (self.y+self.h) > y1 and
                ((x1 <= self.x <= x2) or (x2 <= self.x <= x1)))

