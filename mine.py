import pygame as py
import random

class Mine:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.texture = py.image.load("mine.png")
        self.background = py.image.load("fond.png")
        self.rect = self.texture.get_rect(center=self.texture.get_rect(center=(round(self.x),round(self.y))).center)
        self.screen = screen

    def type(self):
        return Mine
    
    def getRect(self):
        return self.rect
    
    def getHitbox(self):
        return (self.x,self.y,self.x+8,self.y+8)

    def drawBackground(self, background):
        img = background.subsurface(self.rect)
        self.screen.blit(img,self.rect)

    def draw(self):
        self.screen.blit(self.texture,self.rect)