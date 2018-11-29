import os
import sys
import pygame as pg

script_dir = sys.path[0]
img_path = os.path.join(script_dir, 'images/others/')

class Platform(pg.sprite.Sprite):
    def __init__(self, label, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(img_path+label+'.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.w = w 
        self.h = h