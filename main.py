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
score = 0

borderList = []
foesList = []
missileList = []
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

def createBorder(screen:pygame.Surface)->list:
    """
    Create the borders and return them in a list
    """
    L = []
    #Outer borders
    for i in range(3):
        L.append(border(5+425*i,5,0,425,[0,1],"Outer",screen))
        L.append(border(5+425*i,712,0,425,[0,-1],"Outer",screen))
        L.append(border(5,5+238*i,238, 0, [1,0],"Outer",screen))
        L.append(border(1272,5+238*i,238, 0, [-1,0],"Outer",screen))
    #Inner borders
    L.append(border(429,243,0,422,[0,-1],'Inner',screen))
    L.append(border(429,477,0,422,[0,1],'Inner',screen))
    L.append(border(429,243,234,0,[-1,0],'Inner',screen))
    L.append(border(851,243,234,0,[1,0],'Inner',screen))
    return L

def addNewEnnemie(foesList:list,name:str,wave:int,rotation:bool,screen:pygame.Surface):
    """
    Add an ennemy.
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

def new_wave(wave:int,ClockWiseMove:bool,screen:pygame.Surface)->list:
    """
    Create and return a new set of ennemies matching
    the current wave.
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
image_fond = pygame.image.load("fond.png")

###################################################
# Welcome screen with rules                       #
###################################################
BACKGROUND.menu()

screen.blit(image_fond,(0,0))
BACKGROUND.update_life(player)
BACKGROUND.update_score(score)


while ingame:

    pygame.time.delay(5)
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
    if keys == K_x or keys == K_SPACE:
        player.shoot(missileList)
    if keys == K_p:
        BACKGROUND.pause(player)

    #Check continuously pressed keys
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
            foe.move(missileList, foesList, player.getPos())
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
                    foe.bounce(border.getNormalVector())

        if border.collides_with_rect(player):
            player.bounce(border.getNormalVector())
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