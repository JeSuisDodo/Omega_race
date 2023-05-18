import pygame
from pygame.locals import *
import sys
import constants
import spaceship
import font
from border import border
from mine import Mine
from droid import Droid
from mothership import MotherShip
from supership import SuperShip
from random import randint
###################################################
# Variables                                       #
###################################################
ingame = True
pause = False
wave = 0
timeBeforeNextWave = 0
ClockWiseMove = bool(randint(0,1))

borderList = []
foesList = []
missileList = []

###################################################
# Functions                                       #
###################################################
def getKeyDown():
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
    while getKeyDown() == None:
        pygame.display.update()


def leave():
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()

def createBorder(screen)->list:
    """
    Create the borders and return them in a list
    """
    L = []
    #Outer borders
    for i in range(3):
        L.append(border(5+425*i,5,0,425,'x',"Outer",screen))
        L.append(border(5+425*i,712,0,425,'x',"Outer",screen))
        L.append(border(5,5+238*i,238, 0, 'y',"Outer",screen))
        L.append(border(1272,5+238*i,238, 0, 'y',"Outer",screen))
    #Inner borders
    for i in range(2):
        L.append(border(429,243+234*i,0,422,'x','Inner',screen))
        L.append(border(429+422*i,243,234,0,'y','Inner',screen))
    
    return L

def addNewEnnemie(foesList,name,wave,rotation,screen):
    """
    """
    x = randint(9,1239)
    y = randint(478,679)
    
    match name:
        case "droid":
            foesList.append(Droid(x,y,wave,rotation,screen))
        case "mothership":
            foesList.append(MotherShip(x,y,wave,rotation,screen))
        case "supership":
            foesList.append(SuperShip(x,y,wave,rotation,screen))

def new_wave(wave,ClockWiseMove,screen)->list:
    """
    """
    L = []
    #if wave%10==0:
        #L.append(Boss(wave,screen))
    #else
    for i in range(7+wave):
        addNewEnnemie(L,"droid",wave,ClockWiseMove,screen)
    for i in range(1+wave//3):
        addNewEnnemie(L,"mothership",wave,ClockWiseMove,screen)
    for i in range(wave//10):
        addNewEnnemie(L,"supership",wave,ClockWiseMove,screen)
    
    return L

def getPresenceOfSuperEnnemy(foesList):
    info = [False,False]
    for foe in foesList:
        if (isinstance(foe,MotherShip) and foe.getNumberOfTransform() == 
            0) or (isinstance(foe,Droid) and foe.getNumberOfTransform() == 1):
            info[0] = True
        elif isinstance(foe,SuperShip) or (isinstance(foe,
        MotherShip) and foe.getNumberOfTransform() == 
        1) or (isinstance(foe,Droid) and foe.getNumberOfTransform() == 2):
            info[1] = True
    return info

###################################################
# Init                                            #
###################################################
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((constants.WIDTH_SCREEN,constants.HEIGHT_SCREEN))
clock = pygame.time.Clock()
BACKGROUND = font.Fond(screen)
pygame.display.set_caption("Omega Race")
player = spaceship.Spaceship(screen)
borderList = createBorder(screen)
###################################################
# Welcome screen with rules                       #
###################################################

print(ClockWiseMove)
BACKGROUND.menu()

image_fond = pygame.image.load("fond.png")
screen.blit(image_fond,(0,0))
BACKGROUND.update_life(player)
BACKGROUND.update_score(player)
while ingame:

    pygame.time.delay(2)
    clock.tick(120)

    #Pre-draw => draw background on last position
    BACKGROUND.preDraw(player,missileList,foesList,borderList,image_fond)

    #Draw all objects (player, missiles, foes, border)
    player.draw()
    for foe in foesList:
        foe.draw()
    for mis in missileList:
        mis.draw()
    for border in borderList:
        if border.isOuter():
            border.decreaseAlpha(2)
            border.drawAlpha(constants.WHITE)
        else:
            border.draw(constants.WHITE)

    pygame.display.update()

    #Check keys down
    keys = getKeyDown()
    if keys == K_x:
        player.shoot(missileList)
    if keys == K_p:
        BACKGROUND.pause(player)

    #Check continuously pressed keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.booster()
    else:
        player.stop_booster()
    if keys[pygame.K_LEFT]:
        player.turnLeft()
    if keys[pygame.K_RIGHT]:
        player.turnRight()
    

    #Moving ennemies
    for foe in foesList:
        if not(isinstance(foe,Mine)):
            foe.move(missileList, foesList, player.getPos())
    """
    while(len(foesList) < 10):
        foesList.append(mine.Mine(randint(20,1200),randint(500,680),screen))
    for foe in foesList:
        if foe.is_colliding_with_spaceship(player):
            foesList.remove(foe)
            player.life -= 1
            BACKGROUND.update_life(player)
            if player.life == 0:
                BACKGROUND.dead(player)
    """
    #Moving missiles
    for mis in missileList:
        mis.move()
    #Déplacement du joueur
    player.move()


    #Collisions
    for border in borderList:
        for mis in missileList:
            if border.collides_with_line(mis):
                mis.die(image_fond)
                missileList.remove(mis)
        for foe in foesList:
            if isinstance(foe,SuperShip):
                if border.collides_with_rect(foe):
                    foe.bounce(border.getAxis())

        if border.collides_with_rect(player):
            player.bounce(border.getAxis())
            if border.isOuter():
                border.setAlpha(255)
    

    #Check state of wave
    if foesList == []:
        if timeBeforeNextWave <= 0:
            timeBeforeNextWave = 500
            wave += 1
            foesList = new_wave(wave, ClockWiseMove, screen)
        else:
            timeBeforeNextWave -= 1

#Ecran de fin de jeu
leave()