import pygame as py
from random import randint
from missile import Missile
from mine import Mine
from numpy import sin, cos, deg2rad, arccos, rad2deg, log

class SuperShip:
	"""
	Create a super ennemy ship.
	Quick aggressive ennemy which can land mines and shoot
	multiple missiles at a time.

	list[py.Surface] texture : all the textures of the ennemy
	int texturePos : the current texture it displays
	int attackCooldown : time in gameloops before the next attack
	"""
	texture = [py.transform.scale(py.image.load("supership"+str(i)+".png"),
                                  (32,32)) for i in range(1,6)]
	texturePos = 0
	attackCooldown = 500
	
	def __init__(self,x:float,y:float,wave:int,rotation:bool,screen:py.Surface):
		"""
		float x,y : real position of the ennemy
		int posX, posY : rounded position
		int wave : current wave
		float speed : speed of the ennemy based on the wave
		bool rot : tell if the ennemy starts moving clock-wise
		py.Rect rect : current rect object of the ennemy
		py.Surface screen : the screen of the game
		"""
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
		
		self.rect = self.texture[0].get_rect(topleft=(self.posX,self.posY))
		
		self.screen = screen

	def getRect(self)->py.Rect:
		"""
		Return current rect.
		"""
		return self.rect
	
	def draw(self):
		"""
		Draw the current texture on the screen according to the current rect.
		"""
		img = self.texture[self.texturePos//8]

		self.texturePos += 1
		if self.texturePos >= 40:
			self.texturePos = 0
		self.screen.blit(img,self.rect)
	
	def drawBackground(self,background:py.Surface):
		"""
		Draw the image of the background on the last postion of
		the ennemy
		
		py.Surface background : the image of the background
		"""
		img = background.subsurface(self.rect)
		self.screen.blit(img, self.rect)

	def getShootAngle(self,playerPos:tuple[int])->int:
		"""
		Compute and return the shoot angle.
		
		tuple[int] playerPos : rounded player's position
		"""
		px, py = playerPos
		vec = [px - self.posX,py - self.posY]
		normeVec = (vec[0]**2 + vec[1]**2)**0.5
		angle = vec[0]/normeVec #Scalar product by (1,0)
		angle = rad2deg(arccos(angle))

		#This method don't show if the player is above or
		#under the ennemy so we have to compute it after
		if vec[1] > 0:
			return 360 - angle
		return angle

	def attack(self,missileList:list[Missile],foesList:list,playerPos:tuple[int]):
		"""
		The supership attacks. It can land a mine or shoot multiple missiles
		at the player.

		list[Missile] missileList : the list of all the missiles
		list foesList : the list of all the ennemies and the mines
		tuple[int] playerPos : position of the player
		"""
		x = self.posX + 16
		y = self.posY + 16
		if randint(1,5) == 1:
			foesList.append(Mine(x,y,self.screen))
		else:
			shootAngle = self.getShootAngle(playerPos)
			missileList.append(Missile(shootAngle, True, x, y, self.screen))
			missileList.append(Missile(shootAngle+5, True, x, y, self.screen))
			missileList.append(Missile(shootAngle-5, True, x, y, self.screen))
	
	def move(self, missileList:list[Missile], foesList:list, playerPos:tuple[int]):
		"""
		Move the supership.
		Then update the rounded position and the rect.
		Finally, check if it can attack.
		"""
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
	
	def bounce(self, vect:list[int]):
		"""
		The supership bounce on a border.
		Update rounded position and rect.
		
		list[int] vect : normal vector of the border the supership bounced on
		"""
		self.x -= self.speed * self.vector[0]
		self.y -= self.speed * self.vector[1]
		self.x += vect[0]
		self.y += vect[1]
		self.posX = round(self.x)
		self.posY = round(self.y)
		self.rect = self.texture[0].get_rect(topleft=(self.posX,self.posY))

		if vect[0] == 0:
			self.vector[1] *= -1
		else:
			self.vector[0] *= -1
