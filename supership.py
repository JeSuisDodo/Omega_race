import pygame as py
from random import randint
import missile
import mine
from numpy import sin, cos, deg2rad, arctan, rad2deg

class SuperShip:
	"""
	Create a super ennemie ship
	"""
	def __init__(self,x,y,screen):
		self.x = x
		self.y = y
		self.posX = x
		self.posY = y
		angle = [45,135,225,315][randint(0,3)]
		self.vector = [cos(deg2rad(angle)),sin(-deg2rad(angle))]
		self.texture = [py.image.load("supership"+str(i)+".png") for i in range(3)]
		for i in range(len(self.texture)):
			self.texture[i] = py.transform.scale(self.texture[i],(32,32))
		self.texturePos = 0
		self.rect = self.texture[0].get_rect(topleft=(self.posX,self.posY))
		self.attackCooldown = 0
		self.screen = screen
		
	def type(self):
		return SuperShip

	def getRect(self):
		return self.rect
	
	def draw(self):
		img = self.texture[self.texturePos//50]
		self.texturePos += 1
		if self.texturePos >= 150:
			self.texurePos = 0
		self.screen.blit(img,self.rect)
	
	def drawBackground(self,background):
		img = background.subsurface(self.rect)
		self.screen.blit(img, self.rect)

	def findShootAngle(self,playerPos):
		absAngle = arctan(abs(playerPos[1]-self.y)/abs(playerPos[0]-self.x))
		degAngle = rad2deg(absAngle)
		if playerPos[0] < self.x:
			degAngle += 90
		if playerPos[1] < self.y:
			degAngle += 180
		return degAngle

	def attack(self,missileList,foesList,playerPos):
		if self.attackCooldown == 0:
			self.attackCooldown = randint(500,2000)
			if randint(0,2) == 1:
				shootAngle = self.findShootAngle(playerPos)
				missileList.append(missile.Missile(shootAngle, True, self.x, self.y, self.screen))
			else:
				foesList.append(mine.Mine(self.posX,self.posY,self.screen))
		else:
			self.attackCooldown -= 1
	
	def move(self, missileList, foesList, playerPos):
		SPEED = 5
		self.x += SPEED * self.vector[0]
		self.y += SPEED * self.vector[1]
		self.posX = round(self.x)
		self.posY = round(self.y)
		self.rect = self.texture[0].get_rect(topleft=(self.posX,self.posY))
		self.attack(missileList, foesList, playerPos)
	
	def bounce(self, axis):
		if axis == 'x':
			self.vector[1] *= 1
		else:
			self.vector[0] *= -1
