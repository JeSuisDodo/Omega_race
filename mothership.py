import pygame as py
from numpy import log, arccos, rad2deg
from random import randint
from mine import Mine
from missile import Missile
from supership import SuperShip

class MotherShip:
	"""
	Create a mothership
	"""
	texture = [py.image.load("mothership1.png"),py.image.load("mothership2.png")]
	for i in range(len(texture)):
			texture[i] = py.transform.scale(texture[i],(32,32))
	superTexture = py.transform.scale(py.image.load("supership_base.png"),(32,32))
	tranformTime = 750

	def __init__(self,x,y,wave,rotation,screen):
		self.x = x
		self.y = y
		self.posX = x
		self.posY = y
		if rotation:
			self.step = 3
			self.objectiv = randint(9,396)
		else:
			self.step = 2
			self.objectiv = randint(852,1239)
		self.rot = rotation
		self.wave = wave
		self.speed = log(wave+1)*2
		self.texturePos = 0
		self.rect = self.texture[0].get_rect(topleft=(x,y))
		self.lastRect = None
		self.attackCooldown = 0
		self.timeBeforeTransform = randint(1500,3000)
		self.screen = screen

	def getRect(self):
		return self.rect

	def draw(self):
		if self.timeBeforeTransform == 0 and self.tranformTime%40<20:
			self.screen.blit(self.superTexture,self.rect)
		else:
			self.screen.blit(self.texture[self.texturePos//50],self.rect)
		self.texturePos += 1
		if self.texturePos >= 100:
			self.texturePos = 0
	
	def drawBackground(self,background):
		if self.lastRect:
			img = background.subsurface(self.lastRect)
			self.screen.blit(img,self.lastRect)

	def getShootAngle(self,playerPos):
		px, py = playerPos
		vec = [px - self.posX,py - self.posY]
		normeVec = (vec[0]**2 + vec[1]**2)**0.5
		angle = vec[0]/normeVec #Scalar product by (1,0)
		angle = rad2deg(arccos(angle))
		if vec[1] > 0:
			return 360 - angle
		return angle

	def attack(self, missileList, foesList, playerPos):
		if randint(1,3) == 0:
			foesList.append(Mine(self.posX+16,self.posY+16,self.screen))
		else:
			angle = self.getShootAngle(playerPos)
			missileList.append(Missile(angle,True,self.posX+16,self.posY+16,self.screen))

	def objectivReached(self)->bool:
		if self.rot:
			if self.step == 0 and self.posY <= self.objectiv:
				self.objectiv = randint(852,1239)
				return True
			elif self.step == 1 and self.posX >= self.objectiv:
				self.objectiv = randint(478,679)
				return True
			elif self.step == 2 and self.posY >= self.objectiv:
				self.objectiv = randint(9,396)
				return True
			elif self.step == 3 and self.posX <= self.objectiv:
				self.objectiv = randint(9,210)
				return True
		else:
			if self.step == 0 and self.posX <= self.objectiv:
				self.objectiv = randint(478,679)
				return True
			elif self.step == 3 and self.posY >= self.objectiv:
				self.objectiv = randint(852,1239)
				return True
			elif self.step == 2 and self.posX >= self.objectiv:
				self.objectiv = randint(9,210)
				return True
			elif self.step == 1 and self.posY <= self.objectiv:
				self.objectiv = randint(9,396)
				return True
		return False

	def move(self, missileList, foesList, playerPos):
		if self.tranformTime == 0:
			foesList.append(SuperShip(self.posX,self.posY,self.wave,self.rot,self.screen))
			foesList.remove(self)
			return
		elif self.timeBeforeTransform == 0 and self.tranformTime > 0:
			self.tranformTime -= 1
			return
		
		self.timeBeforeTransform -= 1
		if self.objectivReached():
			if self.rot:
				self.step += 1
			else:
				self.step -= 1
			if self.step > 3:
				self.step = 0
			elif self.step < 0:
				self.step = 3
		
		#move to next step
		self.lastRect = self.rect
		if self.rot:
			if self.step%2 == 1:
				self.x -= (self.step-2) * 0.1 * self.speed
			else:
				self.y += (self.step-1) * 0.1 * self.speed
		elif self.step%2 == 0:
			self.x += (self.step-1) * 0.1 * self.speed
		else:
			self.y += (self.step-2) * 0.1 * self.speed

		self.posX = round(self.x)
		self.posY = round(self.y)
		self.rect = self.texture[0].get_rect(topleft=(self.posX,self.posY))

		if self.attackCooldown <= 0:
			self.attackCooldown = randint(400+400/self.wave,500+500/self.wave)
			self.attack(missileList, foesList, playerPos)
		else:
			self.attackCooldown -= 1