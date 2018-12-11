import sys
import pygame as pg

# move up one directory to be able to import the settings and images
sys.path.append("..")
from objects.Button import Button
from settings import *
from images import *

class Intro:
    def __init__(self, game):
        self.game = game

        start = Button('start', 400, 275, 300, 100)
        guide = Button('guide', 400, 400, 300, 100)
        about = Button('about', 400, 525, 300, 100)

        while self.game.status == INTRO:
            self.game.screen.blit(INTRO_BG, ORIGIN)

            for event in pg.event.get():
                pos = pg.mouse.get_pos()

                if event.type == pg.QUIT:
                    print("You quit in the middle of the game!")
                    self.game.running = False
                    quit()
                
                # mouse click
                if event.type == pg.MOUSEBUTTONDOWN:
                    if start.isOver(pos):
                        self.game.status = START
                    elif guide.isOver(pos):
                        self.game.status = GUIDE
                    elif about.isOver(pos):
                        self.game.status = ABOUT

                # mouse hover
                if event.type == pg.MOUSEMOTION:
                    start.isOver(pos)
                    guide.isOver(pos)
                    about.isOver(pos)

            self.game.screen.blit(start.image, (start.x, start.y))
            self.game.screen.blit(guide.image, (guide.x, guide.y))
            self.game.screen.blit(about.image, (about.x, about.y))

            pg.display.flip()