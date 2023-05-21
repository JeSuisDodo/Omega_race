import pygame as py

class Explosion():
    """
    Class of explosion.
    An animation of an explosion.
    
    list[py.Surface] textures : all textures
    """
    textures = [py.transform.scale(py.image.load("explosion"+str(i)+".png"),(32,32)) for i in range(1,7)]

    def __init__(self,coordinates:tuple[int],explosionList:list,screen:py.Surface):
        """
        Create a new explosion object at given coordinates.
        
        int x,y : coordinates
        list[Explosion] expList : list of all explosion
        py.Surface screen : the screen of the game
        py.Rect rect : rect object describing the explosion
        int texturePos : the current texture displayed
        """
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.expList = explosionList
        self.screen = screen
        self.rect = self.textures[0].get_rect(topleft=(self.x,self.y))
        self.texturePos = 0
    
    def draw(self):
        """
        Draw the explosion.
        Increment texturePos.
        If last frame was drawn then it is erase from
        the list of all explosions.
        """
        self.screen.blit(self.textures[self.texturePos//20],self.rect)

        self.texturePos += 1
    
    def drawBackground(self,background:py.Surface):
        """
        Draw background at position.

        py.Surface background : background's image
        """
        img = background.subsurface(self.rect)
        self.screen.blit(img,self.rect)
        if self.texturePos >= 120:
            self.expList.remove(self)