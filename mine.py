import pygame as py

class Mine:
    """
    Class of the mine.
    Mine are stationary ennmies that can hurt the player.
    They are destroyed by shooting at them.
    
    py.Surface texture : texture of the mine
    """
    texture = py.image.load("mine.png")


    def __init__(self, x:int, y:int, screen:py.Surface):
        """
        Create a new Mine object.
        
        int x,y : postion of the mine
        py.Rect rect : rect object describing the mine
        py.Surface screen : screen of the game
        """
        self.x = x
        self.y = y
        self.rect = self.texture.get_rect(center=self.texture.get_rect(center=(round(self.x),round(self.y))).center)
        self.screen = screen
    
    def getRect(self)->py.Rect:
        """
        Return the rect of the mine.
        """
        return self.rect
    
    def getCo(self)->tuple[int]:
        """
        Return a tuple of coordinates
        """
        return (self.x-16,self.y-16)
    
    def getHitbox(self)->tuple[int]:
        """
        Return the top-left and bottom right coordinates of
        the rect made by the missile
        """
        return (self.x,self.y,self.x+8,self.y+8)

    def drawBackground(self, background:py.Surface):
        """
        Draw the background on the mine's position.

        py.Surface background : background's image
        """
        img = background.subsurface(self.rect)
        self.screen.blit(img,self.rect)

    def draw(self):
        """
        Draw the mine on the screen
        """
        self.screen.blit(self.texture,self.rect)