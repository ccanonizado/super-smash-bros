import os
import sys
import pygame as pg

sys.path.append("..")
from settings import *
from images import MARIO

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)

        self.game = game
        self.image = MARIO
        self.rect = self.image.get_rect()
        self.rect.center = (GAME_WIDTH / 2, HEIGHT / 2)
        self.pos = vec(GAME_WIDTH / 2, HEIGHT / 2)
        self.x = 0
        self.y = 0
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def jump(self):
        
        self.rect.x += 1
        collision = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if collision:
            self.vel.y = -VEL
 
    def update(self):

        self.acc = vec(0 ,0.5)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > GAME_WIDTH:
            self.pos.x = GAME_WIDTH - VEL
        if self.pos.x < 0:
            self.pos.x = VEL

        self.rect.midbottom = self.pos
