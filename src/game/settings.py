'''

This file contains all the settings!

Find the correct label if you want to add or modify values.
If the label does not exist for your new value, just create a new one.

'''

import pygame as pg

# game values
TITLE = "Super Smash Bros"
FULL_WIDTH = 1100
GAME_WIDTH = 700
HEIGHT = 700
BG_SIZE = (FULL_WIDTH, HEIGHT) 
ORIGIN = (0,0)
FPS = 60

# game statuses
INTRO = 0
START = 1
GUIDE = 2
ABOUT = 3
GAME = 4

# character movement settings
ACC = 0.5
FRIC = -0.12
VEL = 15

# color settings
BLACK = (0, 0, 0)
BROWN = (45, 33, 19)
BLUE = (59, 148, 238)
WHITE = (255, 255, 255)