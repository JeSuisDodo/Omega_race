import pygame as py
from numpy import log, arccos, rad2deg
from random import randint
from mine import Mine
from missile import Missile
from supership import SuperShip

class MotherShip:
	"""
	Create a mothership.
	Agressive ennemy which can shoot a single missile or land a mine.
	After a while it starts transforming into a supership.

	list[py.Surface] texture : all the texture of the ennemy
	py.Surface motherTexture : texture of the mothership
	int transfromTime : time left in gameloops before it completes
		its transformation
	int texturePos : the current texture it displays
	"""
	texture = [py.image.load("mothership1.png"),py.image.load("mothership2.png")]
	for i in range(len(texture)):
			texture[i] = py.transform.scale(texture[i],(32,32))
	superTexture = py.transform.scale(py.image.load("supership_base.png"),(32,32))
	tranformTime = 750
	texturePos = 0

	def __init__(self,x:float,y:float,wave:int,rotation:bool,screen:py.Surface):
		"""
		float x,y : real position of the ennemy
		int posX, posY : rounded position
		int step : where the ennemy is going
			if 0 -> top left
			if 1 -> top right
			if 2 -> bottom right
			if 3 -> bottom left
		int objectiv : the x or y position the ennemy must reach
			to complete the 'step'
		int wave : current wave
		float speed : speed of the ennemy based on the wave
		bool rot : tell if the ennemy is moving clock-wise
		py.Rect rect : current rect object of the ennemy
		py.Rect lastRect : rect object of the last position
		int attackCooldown : time in gameloops before the next attack
		py.Surface screen : the screen of the game
		int timeBeforeTransform : time left in gameloops before the
			ennemy transform
		"""
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
		self.rect = self.texture[0].get_rect(topleft=(x,y))
		self.lastRect = None
		self.attackCooldown = 500
		self.screen = screen
		self.timeBeforeTransform = randint(2000,3500)

	def getRect(self)->py.Rect:
		"""
		Return the current rect.
		"""
		return self.rect
	
	def getCo(self)->tuple[int]:
		"""
		Return a tuple of rounded coordinates.
		"""
		return (self.posX,self.posY)

	def draw(self):
		"""
		Draw the current texture on the screen according to the current rect.
		If it is transforming then it shows half the time the texture of the
		supership's base.
		"""
		if self.timeBeforeTransform == 0 and self.tranformTime%40<20:
			self.screen.blit(self.superTexture,self.rect)
		else:
			self.screen.blit(self.texture[self.texturePos//50],self.rect)
		
		self.texturePos += 1
		if self.texturePos >= 100:
			self.texturePos = 0
	
	def drawBackground(self,background:py.Surface):
		"""
		Draw the image of the background on the last postion of
		the ennemy
		
		py.Surface background : the image of the background
		"""
		if self.lastRect:
			img = background.subsurface(self.lastRect)
			self.screen.blit(img,self.lastRect)

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

	def attack(self, missileList:list[Missile], foesList:list, playerPos:tuple[int]):
		"""
		The mothership try to attack. It can land a mine or shoot at the player.

		list[Missile] missileList : the list of all the missiles
		list foesList : the list of all the ennemies and the mines
		tuple[int] playerPos : position of the player
		"""
		#Attack if the cooldown if over. Else decreased it by 1.
		if self.attackCooldown <= 0:
			self.attackCooldown = randint(400+round(400/self.wave),500+round(500/self.wave))
			if randint(1,3) == 0:
				foesList.append(Mine(self.posX+16,self.posY+16,self.screen))
			else:
				angle = self.getShootAngle(playerPos)
				missileList.append(Missile(angle,True,self.posX+16,self.posY+16,self.screen))
		else:
			self.attackCooldown -= 1

	def objectivReached(self)->bool:
		"""
		Return True if the ennemy reached the 'step', False else.
		If it has reached the step. Create a new one.
		"""
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

	def move(self, foesList:list):
		"""
		Move the ennemy if it is not during the transformation into a
		supership.
		Then, update the rect and the rounded position.
		
		list foesList : the list of all the ennemies and the mines
		"""
		#Check for transformation
		if self.tranformTime == 0:
			#Delete the object and add a new supership at the same position
			foesList.append(SuperShip(self.posX,self.posY,self.wave,self.rot,self.screen))
			foesList.remove(self)
			return
		elif self.timeBeforeTransform == 0 and self.tranformTime > 0:
			self.tranformTime -= 1
			return
		
		#Update time for transformation
		self.timeBeforeTransform -= 1
		#Check the objectiv
		if self.objectivReached():
			if self.rot:
				self.step += 1
			else:
				self.step -= 1
			if self.step > 3:
				self.step = 0
			elif self.step < 0:
				self.step = 3
		
		#Remember the last rect
		self.lastRect = self.rect
		#Move to next step
		if self.rot:
			if self.step%2 == 1:
				self.x -= (self.step-2) * 0.1 * self.speed
			else:
				self.y += (self.step-1) * 0.1 * self.speed
		elif self.step%2 == 0:
			self.x += (self.step-1) * 0.1 * self.speed
		else:
			self.y += (self.step-2) * 0.1 * self.speed

		#Update rounded positiion and rect
		self.posX = round(self.x)
		self.posY = round(self.y)
		self.rect = self.texture[0].get_rect(topleft=(self.posX,self.posY))