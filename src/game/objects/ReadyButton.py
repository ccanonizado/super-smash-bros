'''

This is similar to Button.py but when clicked - the old image stays.
'''

import os
import sys
import pygame as pg

# add the path to the folder with the button images
script_dir = sys.path[0]
img_path = os.path.join(script_dir, 'images/buttons/')

class ReadyButton:
    def __init__(self, label, x, y, w, h):
        self.label = label
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pg.image.load(img_path+label+'a.png')
        self.clicked = False

    # returns True and changes image if mouse is inside button
    # else returns False and retains original image
    def isOver(self, pos):
        # pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                if self.clicked:
                    self.image = pg.image.load(img_path+self.label+'a.png')
                else:
                    self.image = pg.image.load(img_path+self.label+'b.png')
                return True

        if self.clicked:
            self.image = pg.image.load(img_path+self.label+'b.png')
        else:
            self.image = pg.image.load(img_path+self.label+'a.png')
        return False

    def click(self):
        if not self.clicked:
            self.clicked = True
        else:
            self.clicked = False
    