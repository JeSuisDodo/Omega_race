import pygame as py
from random import randint
import missile
import mine
from numpy import sin, cos, deg2rad, arccos, rad2deg, log

class SuperShip:
	"""
	Create a super ennemie ship
	"""
	texture = [py.transform.scale(py.image.load("supership"+str(i)+".png"),
                                  (32,32)) for i in range(1,6)]
	
	def __init__(self,x,y,wave,rotation,screen):
		self.x = x
		self.y = y
		self.posX = x
		self.posY = y
		if rotation:
			angle = [135,225][randint(0,1)]
		else:
			angle = [45,315][randint(0,1)]
		self.vector = [cos(deg2rad(angle)),sin(-deg2rad(angle))]
		self.wave = wave
		self.speed = log(wave+1)*3
		self.rot = rotation
		self.texturePos = 0
		self.rect = self.texture[0].get_rect(topleft=(self.posX,self.posY))
		self.attackCooldown = 0
		self.screen = screen

	def getRect(self):
		return self.rect
	
	def draw(self):
		img = self.texture[self.texturePos//8]
		self.texturePos += 1
		if self.texturePos >= 40:
			self.texturePos = 0
		self.screen.blit(img,self.rect)
	
	def drawBackground(self,background):
		img = background.subsurface(self.rect)
		self.screen.blit(img, self.rect)

	def getShootAngle(self,playerPos):
		px, py = playerPos
		vec = [px - self.posX,py - self.posY]
		normeVec = (vec[0]**2 + vec[1]**2)**0.5
		angle = vec[0]/normeVec #Scalar product by (1,0)
		angle = rad2deg(arccos(angle))
		if vec[1] > 0:
			return 360 - angle
		return angle

	def attack(self,missileList,foesList,playerPos):
		x = self.posX + 16
		y = self.posY + 16
		if randint(1,3) == 1:
			foesList.append(mine.Mine(x,y,self.screen))
		else:
			shootAngle = self.getShootAngle(playerPos)
			missileList.append(missile.Missile(shootAngle, True, x, y, self.screen))
			missileList.append(missile.Missile(shootAngle+5, True, x, y, self.screen))
			missileList.append(missile.Missile(shootAngle-5, True, x, y, self.screen))
	
	def move(self, missileList, foesList, playerPos):
		self.x += self.speed * self.vector[0]
		self.y += self.speed * self.vector[1]
		self.posX = round(self.x)
		self.posY = round(self.y)
		self.rect = self.texture[0].get_rect(topleft=(self.posX,self.posY))
		if self.attackCooldown <= 0:
			self.attackCooldown = randint(400+400/self.wave,500+500/self.wave)
			self.attack(missileList, foesList, playerPos)
		else:
			self.attackCooldown -= 1
	
	def bounce(self, axis):
		if axis == 'x':
			self.vector[1] *= -1
		else:
			self.vector[0] *= -1
