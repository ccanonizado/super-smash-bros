import sys
import pygame as pg

# move up one directory to be able to import the settings and images
sys.path.append("..")
from objects.Button import Button
from settings import *
from images import *

class Other:
    def __init__(self, game, flag, bg):
        self.game = game
        
        back = Button('back', 20, 20, 100, 100)

        while self.game.status == flag:
            self.game.screen.blit(bg, ORIGIN)

            for event in pg.event.get():
                pos = pg.mouse.get_pos()

                if event.type == pg.QUIT:
                    print("You quit in the middle of the game!")
                    self.game.running = False
                    quit()
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if back.isOver(pos):
                        self.game.status = INTRO
                        break

                if event.type == pg.MOUSEMOTION:
                    back.isOver(pos)

            self.game.screen.blit(back.image, (back.x, back.y))

            pg.display.flip()
