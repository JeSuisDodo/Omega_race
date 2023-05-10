import pygame as py

class MotherShip:
	"""
	Create a mothership
	"""
	def __init__(self,x,y,screen):
		self.x = x
		self.y = y
		self.texture = [py.image.load("mothership1.png"),py.image.load("mothership2.png")]
		for i in range(len(self.texture)):
			self.texture[i] = py.transform.scale(self.texture[i],(32,32))
		self.texturePos = 0
		self.rect = self.texture[0].get_rect(topleft=(self.x,self.y))
		self.screen = screen

	def type(self):
		return MotherShip

	def getRect(self):
		return self.rect

	def draw(self):
		self.screen.blit(self.texture[self.texturePos//50],self.rect)
		self.texturePos += 1
		if self.texturePos >= 100:
			self.texturePos = 0
	
	def drawBackground(self,background):
		img = background.subsurface(self.rect)
		self.screen.blit(img,self.rect)

	def attack(self, missileList, foesList, playerPos):
		pass

	def move(self, missileList, foesList, playerPos):
		self.attack(missileList, foesList, playerPos)
	
	def bounce(self, axis):
		pass