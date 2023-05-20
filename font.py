import pygame
import sys
import constants
import random
import border
from numpy import cos, sin, deg2rad
from pygame.locals import *
import spaceship
from math import floor
import mine

def getKeyDown():
    for event in pygame.event.get():
        global ingame
        if event.type == pygame.QUIT:  # N'a pas l'air de fonctionner
            ingame = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                ingame = False
            return event.key
        return None


class Star:
    """
    Create a missile object
    """

    def __init__(self, screen):
        self.x = random.randint(0, 1250)
        self.y = random.randint(0,700)
        self.posX = self.x
        self.posY = 0
        self.angle = random.randint(190, 350)
        self.screen = screen
        self.image = pygame.image.load("stars.png")

    def type(self):
        return Star

    def move(self):
        self.x += 1/10 * cos(deg2rad(self.angle))
        self.y -= 1/10 * sin(deg2rad(self.angle))
        self.posX = round(self.x)
        self.posY = round(self.y)

    def draw(self):
        self.screen.blit(self.image,(self.x,self.y))
    

class Fond:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.music = "musique.mp3"
        self.font = pygame.image.load("fond.png")
        
    def menu(self):

        color_play = constants.RED
        police_play = pygame.font.Font(None, 70)
        play_text = police_play.render("Play", True, color_play)
        playRect = play_text.get_rect()
        playRect.center = (constants.Center[0], constants.Center[1])

        police_para = pygame.font.Font(None, 50)
        parametres_text = police_para.render(
            "Paramètres", True, constants.WHITE)
        parametresRect = parametres_text.get_rect()
        parametresRect.center = (1150, 50)

        leaveWHITE = pygame.image.load("leave.png")
        leaveRED = pygame.image.load("leave2.png")

        

        leaveRED_Rect = leaveRED.get_rect()
        leaveRED_Rect.center = (25,25)

        stars = [Star(self.screen) for i in range(50)]

        menu = True
        while menu:
            
            keys = getKeyDown()
            mouse_pos = pygame.mouse.get_pos()

            if playRect.collidepoint(mouse_pos):
                color_play = constants.WHITE
                if pygame.mouse.get_pressed()[0]:
                    menu = False
            else:
                color_play = constants.RED

            if parametresRect.collidepoint(mouse_pos):
                color_para = constants.WHITE
            else:
                color_para = constants.RED

            police_play = pygame.font.Font(None, 70)
            play_text = police_play.render("Play", True, color_play)
            playRect = play_text.get_rect()
            playRect.center = (constants.Center[0], constants.Center[1])

            police_para = pygame.font.Font(None, 50)
            parametres_text = police_para.render(
                "Paramètres", True, color_para)
            parametresRect = parametres_text.get_rect()
            parametresRect.center = (1150, 50)

            self.screen.fill(constants.BLACK)
            self.screen.blit(play_text, playRect)
            self.screen.blit(parametres_text, parametresRect)

            if leaveRED_Rect.collidepoint(mouse_pos):
                self.screen.blit(leaveWHITE,(10,10))
                if pygame.mouse.get_pressed()[0]:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
            else:
                self.screen.blit(leaveRED,(10,10))

            for star in stars:
                star.draw()
                star.move()
                if star.x > 1280 :
                    star.x = 0
                elif star.x < 0:
                    star.x = 1280
                if star.y > 720:
                    star.y = 0

            pygame.display.update()



    def border_font(self,border):
        x,y = border.x,border.y
        co_x,co_y = floor(x/80),floor(y/80)
        if border.axis == 'x':
                for i in range(6):
                    self.screen.blit(self.font[co_y][co_x + i],((co_x + i)*80,co_y*80))
        else:
            for i in range(3):
                    self.screen.blit(self.font[co_y + i][co_x],(co_x*80,(co_y + i)*80))

    def update_score(self,score):

        police_score = pygame.font.Font(None, 30)
        score_text = police_score.render("Score : " + str(score), True, constants.WHITE)
        scoreRect = score_text.get_rect()
        scoreRect.center = (constants.Center[0], constants.Center[1]-30)
        self.screen.blit(score_text,scoreRect)

    def update_life(self,player):

        life = pygame.image.load("spaceship.png")
        lifeRect = life.get_rect()
        for i in range(player.life):
            self.screen.blit(life,(constants.Center[0] + 8000 - 20*i,constants.Center[1] - 20))


    def pause(self,player):

        police_play = pygame.font.Font(None, 70)
        play_text = police_play.render("Resume", True, constants.WHITE)
        playRect = play_text.get_rect()
        playRect.center = (constants.Center[0], constants.Center[1]-50)

        police_para = pygame.font.Font(None, 50)
        parametres_text = police_para.render("Settings", True, constants.WHITE)
        parametresRect = parametres_text.get_rect()
        parametresRect.center = (constants.Center[0], constants.Center[1])

        police_leave = pygame.font.Font(None, 50)
        leave_text = police_leave.render("Leave", True, constants.WHITE)
        leaveRect = leave_text.get_rect()
        leaveRect.center = (constants.Center[0], constants.Center[1]+50)
        
        stars = [Star(self.screen) for i in range(50)]

        pause = True
        while pause:
            
            keys = getKeyDown()
            mouse_pos = pygame.mouse.get_pos()

            if playRect.collidepoint(mouse_pos):
                color_play = constants.WHITE
                if pygame.mouse.get_pressed()[0]:
                    pause = False
            else:
                color_play = constants.RED

            if parametresRect.collidepoint(mouse_pos):
                color_para = constants.WHITE
            else:
                color_para = constants.RED
            
            if leaveRect.collidepoint(mouse_pos):
                color_leave = constants.WHITE
                if pygame.mouse.get_pressed()[0]:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
            else:
                color_leave = constants.RED

            police_play = pygame.font.Font(None, 70)
            play_text = police_play.render("Resume", True, color_play)
            playRect = play_text.get_rect()
            playRect.center = (constants.Center[0], constants.Center[1]-50)

            police_para = pygame.font.Font(None, 50)
            parametres_text = police_para.render("Settings", True, color_para)
            parametresRect = parametres_text.get_rect()
            parametresRect.center = (constants.Center[0], constants.Center[1])

            police_leave = pygame.font.Font(None, 50)
            leave_text = police_leave.render("Leave", True, color_leave)
            leaveRect = leave_text.get_rect()
            leaveRect.center = (constants.Center[0], constants.Center[1]+50)

            self.screen.fill(constants.BLACK)
            self.screen.blit(play_text, playRect)
            self.screen.blit(parametres_text, parametresRect)
            self.screen.blit(leave_text, leaveRect)


            for star in stars:
                star.draw()
                star.move()
                if star.x > 1280 :
                    star.x = 0
                elif star.x < 0:
                    star.x = 1280
                if star.y > 720:
                    star.y = 0

            pygame.display.update()
        
        image = pygame.image.load("fond.png")
        self.screen.blit(image,(0,0))
        self.update_life(player)
        self.update_score(player)

    def dead(self,player):
        
        police_play = pygame.font.Font(None, 70)
        play_text = police_play.render("Retry", True, constants.WHITE)
        playRect = play_text.get_rect()
        playRect.center = (constants.Center[0], constants.Center[1]-50)

        police_leave = pygame.font.Font(None, 50)
        leave_text = police_leave.render("Leave", True, constants.WHITE)
        leaveRect = leave_text.get_rect()
        leaveRect.center = (constants.Center[0], constants.Center[1]+50)
        
        stars = [Star(self.screen) for i in range(50)]

        pause = True
        while pause:
            
            keys = getKeyDown()
            mouse_pos = pygame.mouse.get_pos()

            if playRect.collidepoint(mouse_pos):
                color_play = constants.WHITE
                if pygame.mouse.get_pressed()[0]:
                    pause = False
            else:
                color_play = constants.RED
            
            if leaveRect.collidepoint(mouse_pos):
                color_leave = constants.WHITE
                if pygame.mouse.get_pressed()[0]:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
            else:
                color_leave = constants.RED

            police_play = pygame.font.Font(None, 70)
            play_text = police_play.render("Resume", True, color_play)
            playRect = play_text.get_rect()
            playRect.center = (constants.Center[0], constants.Center[1]-50)

            police_leave = pygame.font.Font(None, 50)
            leave_text = police_leave.render("Leave", True, color_leave)
            leaveRect = leave_text.get_rect()
            leaveRect.center = (constants.Center[0], constants.Center[1]+50)

            self.screen.fill(constants.BLACK)
            self.screen.blit(play_text, playRect)
            self.screen.blit(leave_text, leaveRect)

            

            for star in stars:
                star.draw()
                star.move()
                if star.x > 1280 :
                    star.x = 0
                elif star.x < 0:
                    star.x = 1280
                if star.y > 720:
                    star.y = 0

            pygame.display.update()
        player.life = 3
        self.update_life
        player.score = 0
        self.update_score
        image = pygame.image.load("fond.png")
        self.screen.blit(image,(0,0))

    def preDraw(self,player,Missiles,Foes,Borders,background):
        player.drawBackground(background)
        for Mi in Missiles:
            Mi.drawBackground(background)
        for foe in Foes:
            foe.drawBackground(background)
        for border in Borders:
            border.drawBackground(background)
        
        