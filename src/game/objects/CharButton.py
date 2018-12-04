'''

This is similar to Button.py but this has preloaded button images.
A similar class has been made for optimization of the character selection screen.

'''

import os
import pygame as pg

# add the path to the folder with the button images
img_path = os.path.abspath(os.curdir) + '/images/buttons/'

marioa = pg.image.load(img_path+'marioa.png') 
mariob = pg.image.load(img_path+'mariob.png')
luigia = pg.image.load(img_path+'luigia.png')
luigib = pg.image.load(img_path+'luigib.png')
yoshia = pg.image.load(img_path+'yoshia.png')
yoshib = pg.image.load(img_path+'yoshib.png')
popoa = pg.image.load(img_path+'popoa.png')
popob = pg.image.load(img_path+'popob.png')
nanaa = pg.image.load(img_path+'nanaa.png')
nanab = pg.image.load(img_path+'nanab.png')
linka = pg.image.load(img_path+'linka.png')
linkb = pg.image.load(img_path+'linkb.png')

class CharButton:
    def __init__(self, label, x, y, w, h):
        self.label = label
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        if label == 'mario':
            self.image = marioa
        elif label == 'luigi':
            self.image = luigia
        elif label == 'yoshi':
            self.image = yoshia
        elif label == 'popo':
            self.image = popoa
        elif label == 'nana':
            self.image = nanaa
        elif label == 'link':
            self.image = linka

    # returns True and changes image if mouse is inside button
    # else returns False and retains original image
    def isOver(self, pos, label):
        # pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                if label == 'mario':
                    self.image = mariob
                elif label == 'luigi':
                    self.image = luigib
                elif label == 'yoshi':
                    self.image = yoshib
                elif label == 'popo':
                    self.image = popob
                elif label == 'nana':
                    self.image = nanab
                elif label == 'link':
                    self.image = linkb
                return True

        if label == 'mario':
            self.image = marioa
        elif label == 'luigi':
            self.image = luigia
        elif label == 'yoshi':
            self.image = yoshia
        elif label == 'popo':
            self.image = popoa
        elif label == 'nana':
            self.image = nanaa
        elif label == 'link':
            self.image = linka
        return False