import os
import sys
import pygame as pg

script_dir = sys.path[0]
img_path = os.path.join(script_dir, 'images/buttons/')

class Button:
    def __init__(self, label, x, y, w, h):
        self.label = label
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pg.image.load(img_path+label+'a.png')

    # returns True and changes image if mouse is inside button
    # else returns False and retains original image
    def isOver(self, pos):
        # pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                self.image = pg.image.load(img_path+self.label+'b.png')
                return True

        self.image = pg.image.load(img_path+self.label+'a.png')
        return False