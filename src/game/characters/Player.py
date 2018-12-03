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

class Player(pg.sprite.Sprite):
    def __init__(self, game, curr_player, name, status, health, pos, direc, walk_c, move):
        pg.sprite.Sprite.__init__(self)

        self.curr_player = curr_player
        self.name = name
        self.status = status
        self.health = health
        self.pos = pos
        self.direc = direc
        self.walk_c = 0
        self.move = move

        self.game = game
        self.image = maS1
        self.rect = self.image.get_rect()
        self.rect.center = (GAME_WIDTH / 2, HEIGHT / 2)
        self.w = self.image.get_size()[0]
        self.h = self.image.get_size()[1]
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

        # block any movement if player pressed 'Enter' to chat
        if not self.game.chatting and self.curr_player == self.name:
            if self.walk_c == 7:
                self.walk_c = 0 

            if keys[pg.K_UP]:
                self.jump()
                self.walk_c = 0

            if keys[pg.K_LEFT]:
                self.acc.x = -ACC
                self.walk_c += 1
                self.direc = LEFT
                self.move = WALK

            elif keys[pg.K_RIGHT]:
                self.acc.x = ACC
                self.walk_c += 1
                self.direc = RIGHT
                self.move = WALK

            else:
                self.walk_c = 0
                self.move = STAND

        # updating the images section
        if self.move == WALK:
            if self.direc == LEFT:
                self.image = walkL[self.walk_c]
            elif self.direc == RIGHT:
                self.image = walkR[self.walk_c]
        
        elif self.move == STAND:
            if self.direc == LEFT:
                self.image = standL
            elif self.direc == RIGHT:
                self.image = standR


        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > GAME_WIDTH:
            self.pos.x = GAME_WIDTH - VEL
        if self.pos.x < 0:
            self.pos.x = VEL

        self.rect.midbottom = self.pos
