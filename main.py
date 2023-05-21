import pygame
from pygame.locals import *
import sys
import constants
from spaceship import Spaceship
import font
from border import Border
from mine import Mine
from droid import Droid
from mothership import MotherShip
from supership import SuperShip
from explosion import Explosion
from missile import Missile
from random import randint
###################################################
# Variables                                       #
###################################################
ingame : bool = True
pause : bool = False
wave : int = 1
waveOver : bool = False
timeBeforeNextWave : int = 500
timeBeforeRestartWave : int = 150
ClockWiseMove : bool = bool(randint(0,1))
score : int = 0
isPlayerHit : bool = False
life : int = 2
###################################################
# Functions                                       #
###################################################
def getKeyDown()->list:
    """
    Return pressed keys
    If the quit button is pressed, leave the game.
    """
    for event in pygame.event.get():
        global ingame
        if event.type == pygame.QUIT: #N'a pas l'air de fonctionner
            ingame = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                ingame = False
            return event.key
        return None

def wait():
    """
    Wait for the player to touch a key.
    """
    while getKeyDown() == None:
        pygame.display.update()

def leave():
    """
    Quit pygame.
    """
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()

def createBorder(screen:pygame.Surface)->list[Border]:
    """
    Create the borders and return them in a list
    """
    l : list[Border] = []
    #Outer borders
    for i in range(3):
        l.append(Border(5+425*i,5,0,425,[0,1],"Outer",screen))
        l.append(Border(5+425*i,712,0,425,[0,-1],"Outer",screen))
        l.append(Border(5,5+238*i,238, 0, [1,0],"Outer",screen))
        l.append(Border(1272,5+238*i,238, 0, [-1,0],"Outer",screen))
    #Inner borders
    l.append(Border(429,243,0,422,[0,-1],'Inner',screen))
    l.append(Border(429,477,0,422,[0,1],'Inner',screen))
    l.append(Border(429,243,234,0,[-1,0],'Inner',screen))
    l.append(Border(851,243,234,0,[1,0],'Inner',screen))
    return l

def addNewEnnemie(foesList:list,name:str,wave:int,rotation:bool,screen:pygame.Surface):
    """
    Add an ennemy.
    """
    x : int = randint(9,1239)
    y : int = randint(478,679)
    
    match name:
        case "droid":
            foesList.append(Droid(x,y,wave,rotation,screen))
        case "mothership":
            foesList.append(MotherShip(x,y,wave,rotation,screen))
        case "supership":
            foesList.append(SuperShip(x,y,wave,rotation,screen))

def new_wave(wave:int,ClockWiseMove:bool,screen:pygame.Surface)->list[Droid|MotherShip|SuperShip]:
    """
    Create and return a new set of ennemies matching
    the current wave.
    """
    l : list[Droid|MotherShip|SuperShip] = []
    #if wave%10==0:
        #l.append(Boss(wave,screen))
    #else
    for i in range(6+wave):
        addNewEnnemie(l,"droid",wave,ClockWiseMove,screen)
    for i in range(1+wave//3):
        addNewEnnemie(l,"mothership",wave,ClockWiseMove,screen)
    for i in range(wave//10):
        addNewEnnemie(l,"supership",wave,ClockWiseMove,screen)
    return l

def rectCollideRect(object1,object2)->bool:
    """
    Return True if the rects collides with each other.
    """
    return object1.getRect().colliderect(object2.getRect())

def rectCollideLine(objectRect,objectLine)->bool:
    """
    Return True if the line touch the rect.
    """
    return objectRect.getRect().clipline(objectLine.getHitbox())

def waveDone(foesList:list[Mine|Droid|MotherShip|SuperShip])->bool:
    for foe in foesList:
        if not(isinstance(foe,Mine)):
            return False
    return True
###################################################
# Init                                            #
###################################################
pygame.init()
pygame.font.init()
screen : pygame.Surface = pygame.display.set_mode((constants.WIDTH_SCREEN,constants.HEIGHT_SCREEN))
clock = pygame.time.Clock()
BACKGROUND = font.Fond(screen)
pygame.display.set_caption("Omega Race")
player : Spaceship = Spaceship(screen)
borderList : list[Border] = createBorder(screen)
foesList : list[Droid|MotherShip|SuperShip|Mine] = new_wave(wave,ClockWiseMove,screen)
missileList : list[Missile] = []
explosionList : list[Explosion] = []
background : pygame.Surface = pygame.image.load("fond.png")

###################################################
# Welcome screen with rules                       #
###################################################
BACKGROUND.menu()

screen.blit(background,(0,0))
BACKGROUND.update_life(player)
BACKGROUND.update_score(score)


while ingame:

    pygame.time.delay(5)
    clock.tick(120)

    #Draw background on last position
    if player:
        player.drawBackground(background)
    for Mi in missileList:
        Mi.drawBackground(background)
    for foe in foesList:
        foe.drawBackground(background)
    for border in borderList:
        border.drawBackground(background)
    for explosion in explosionList:
        explosion.drawBackground(background)

    #Draw all objects (player, missiles, foes, border, explosions)
    if player:
        player.draw()
    for foe in foesList:
        foe.draw()
    for mis in missileList:
        mis.draw()
    for explo in explosionList:
        explo.draw()
    for border in borderList:
        if border.isOuter():
            border.decreaseAlpha(2)
            border.drawAlpha(constants.WHITE)
        else:
            border.draw(constants.WHITE)

    pygame.display.update()
    
    #Check keys down
    keys = getKeyDown()
    if player and (keys == K_x or keys == K_SPACE):
        player.shoot(missileList)
    if keys == K_p:
        BACKGROUND.pause(player)

    #Check continuously pressed keys
    if player:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.start_booster()
        else:
            player.stop_booster()
        if keys[pygame.K_LEFT]:
            player.turnLeft()
        if keys[pygame.K_RIGHT]:
            player.turnRight()
    

    #Moving ennemies
    for foe in foesList:
        if not(isinstance(foe,Mine)):
            foe.move(foesList)
            if player and not(isinstance(foe,Droid)):
                foe.attack(missileList, foesList, player.getPos())
    #Moving missiles
    for mis in missileList:
        mis.move()
    #Moving player
    if player:
        player.move()


    #Collisions
    for border in borderList:
        for mis in missileList:
            if border.collides_with_line(mis):
                mis.die(background)
                missileList.remove(mis)
        for foe in foesList:
            if isinstance(foe,SuperShip):
                if border.collides_with_rect(foe):
                    foe.bounce(border.getNormalVector())

        if player and border.collides_with_rect(player):
            player.bounce(border.getNormalVector())
            if border.isOuter():
                border.setAlpha(255)
    
    for mis in missileList:
        if mis.fromPlayer():
            for foe in foesList:
                if rectCollideLine(foe,mis):
                    mis.die(background)
                    missileList.remove(mis)
                    if isinstance(foe,Droid):
                        score += 500
                    elif isinstance(foe,MotherShip):
                        score += 750
                    elif isinstance(foe,SuperShip):
                        score += 1250
                    
                    BACKGROUND.update_score(score)
                    foe.drawBackground(background)
                    explosionList.append(Explosion(foe.getCo(),explosionList,screen))
                    foesList.remove(foe)
        else:
            if player and rectCollideLine(player,mis):
                isPlayerHit = True
    
    for foe in foesList:
        if player and rectCollideRect(foe,player):
            isPlayerHit = True
    
    #Check player dead
    if isPlayerHit:
        life -= 1
        player.drawBackground(background)
        explosionList.append(Explosion(player.getPos(),explosionList,screen))
        isPlayerHit = False
        player = None
    
    #Restart wave
    if not player:
        if timeBeforeRestartWave <= 0:
            #if life < 0:
            #    BACKGROUND.end()
            #else:
                timeBeforeRestartWave = 150
                timeBeforeNextWave = 300
                pygame.time.delay(1500)
                screen.blit(background,(0,0))
                player = Spaceship(screen)
                foesList = new_wave(wave,ClockWiseMove,screen)
                missileList = []
                explosionList = []
                waveOver = False
                continue
        else:
            timeBeforeRestartWave -= 1

    #Check state of wave
    if waveDone(foesList):
        waveOver = True
    
    if waveOver:
        if timeBeforeNextWave <= 0:
            timeBeforeNextWave = 300
            wave += 1
            screen.blit(background,(0,0))
            pygame.time.delay(1500)
            player = Spaceship(screen)
            foesList = new_wave(wave, ClockWiseMove, screen)
            missileList = []
            explosionList = []
            waveOver = False
            timeBeforeRestartWave = 150
        else:
            timeBeforeNextWave -= 1

#Ecran de fin de jeu
leave()