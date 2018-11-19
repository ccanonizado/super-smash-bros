import pygame
import random
import os
from settings import *

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.image = pygame.image.load(os.path.join(img_folder,"test"))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.x = 0
        self.y = 0
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def jump(self):
        
        self.rect.x += 1
        collision = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if collision:
            self.vel.y = -VEL
 
    def update(self):

        self.acc = vec(0 ,0.5)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = WIDTH - VEL
        if self.pos.x < 0:
            self.pos.x = VEL

        self.rect.midbottom = self.pos

    

class Base(pygame.sprite.Sprite):
    
    def __init__(self, x, y, w, h):
        #self.image = pygame.image.load(os.path.join(img_folder,"platformx.png"))
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w,h))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
