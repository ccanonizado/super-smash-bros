import os
import sys
import pygame as pg

script_dir = sys.path[0]
img_path = os.path.join(script_dir, 'images/buttons/')

# reference for the button - https://www.youtube.com/watch?v=4_9twnEduFA

class Button:
    def __init__(self, label, x, y, w, h):
        self.label = label
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = pg.image.load(img_path+label+'a.png')

    def isOver(self, pos):
        # pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                self.img = pg.image.load(img_path+self.label+'b.png')
                return True

        self.img = pg.image.load(img_path+self.label+'a.png')
        return False