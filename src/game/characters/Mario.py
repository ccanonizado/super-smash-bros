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
weakR = maW1
weakL = pg.transform.flip(weakR, True, False)
heavyR = maH1
heavyL = pg.transform.flip(heavyR, True, False)
damagedR = maD1
damagedL = pg.transform.flip(damagedR, True, False)

class Mario(pg.sprite.Sprite):
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

        # character dependent
        self.weak = 5
        self.heavy = 10
        self.acce = 0.5

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

    def weakAttack(self):
        collided_enemies = pg.sprite.spritecollide(self, self.game.enemy_sprites, False)
        for enemy in collided_enemies:
            enemy.health -= self.weak
            enemy.move = DAMAGED
            self.game.attackPlayer(enemy.name, self.weak, DAMAGED)
            if enemy.health < 0:
                enemy.health = 0

    def heavyAttack(self):
        collided_enemies = pg.sprite.spritecollide(self, self.game.enemy_sprites, False)
        for enemy in collided_enemies:
            enemy.health -= self.heavy
            enemy.move = DAMAGED
            self.game.attackPlayer(enemy.name, self.heavy, DAMAGED)
            if enemy.health < 0:
                enemy.health = 0
 
    def update(self):
        self.acc = vec(0 ,0.5)
        keys = pg.key.get_pressed()

        # block any movement if player pressed 'Enter' to chat
        if not self.game.chatting and self.curr_player == self.name:
            if self.health > 0:
                if self.walk_c == 7:
                    self.walk_c = 0 

                if keys[pg.K_UP]:
                    self.jump()
                    self.walk_c = 0

                if keys[pg.K_LEFT] and self.pos[0] > 40:
                    self.acc.x = -self.acce
                    self.walk_c += 1
                    self.direc = LEFT
                    self.move = WALK

                elif keys[pg.K_RIGHT] and self.pos[0] < GAME_WIDTH-40:
                    self.acc.x = self.acce
                    self.walk_c += 1
                    self.direc = RIGHT
                    self.move = WALK

                else:
                    self.walk_c = 0
                    self.move = STAND

                if keys[pg.K_z]:
                    self.move = WEAK_ATTACK
                
                elif keys[pg.K_x]:
                    self.move = HEAVY_ATTACK

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

        elif self.move == WEAK_ATTACK:
            if self.direc == LEFT:
                self.image = weakL
            elif self.direc == RIGHT:
                self.image = weakR

        elif self.move == HEAVY_ATTACK:
            if self.direc == LEFT:
                self.image = heavyL
            elif self.direc == RIGHT:
                self.image = heavyR
        
        elif self.move == DAMAGED:
            if self.direc == LEFT:
                self.image = damagedL
            elif self.direc == RIGHT:
                self.image = damagedR

        if self.health == 0:
            self.image = dead

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos
