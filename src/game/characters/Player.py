import os
import sys
import pygame as pg

# move up one directory to be able to import the settings and images
sys.path.append("..")
from settings import *
from images import *

vec = pg.math.Vector2

walkR = [maS1, maM1, maM2, maM3, maM4, maM5, maM6, maM7]
walkL = [pg.transform.flip(image, True, False) for image in walkR]
standR = maS1
standL = pg.transform.flip(standR, True, False)

LEFT = 'left'
RIGHT = 'right'

class Player(pg.sprite.Sprite):
    def __init__(self, game, pos):
        pg.sprite.Sprite.__init__(self)

        self.game = game
        self.image = maS1
        self.rect = self.image.get_rect()
        self.rect.center = (GAME_WIDTH / 2, HEIGHT / 2)
        self.pos = pos
        self.w = self.image.get_size()[0]
        self.h = self.image.get_size()[1]
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        self.walkCount = 0
        self.direction = RIGHT

    def jump(self):
        self.rect.x += 1
        collision = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if collision:
            self.vel.y = -VEL
 
    def update(self):
        self.acc = vec(0 ,0.5)
        keys = pg.key.get_pressed()

        # block any movement if player pressed 'Enter' to chat
        if not self.game.chatting:
            if self.walkCount+1 >= 24:
                self.walkCount = 0 

            if keys[pg.K_UP]:
                self.jump()
                self.walkCount = 0

            if keys[pg.K_LEFT]:
                self.acc.x = -ACC
                self.walkCount += 1
                self.direction = LEFT
                self.image = walkL[self.walkCount//3]

            elif keys[pg.K_RIGHT]:
                self.acc.x = ACC
                self.walkCount += 1
                self.direction = RIGHT
                self.image = walkR[self.walkCount//3]

            else:
                if self.direction == RIGHT:
                    self.image = standR
                elif self.direction == LEFT: 
                    self.image = standL
                self.walkCount = 0 

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > GAME_WIDTH:
            self.pos.x = GAME_WIDTH - VEL
        if self.pos.x < 0:
            self.pos.x = VEL

        self.rect.midbottom = self.pos
