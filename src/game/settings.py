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
GUIDE = 1
ABOUT = 2
START = 3
WAITING = 4
GAME = 5

# characters
MARIO = 0
LUIGI = 1
YOSHI = 2
POPO = 3
NANA = 4
LINK = 5

# character movement settings
ACC = 0.5
FRIC = -0.12
VEL = 15

# color settings
BLACK = (0, 0, 0)
BROWN = (45, 33, 19)
BLUE = (59, 148, 238)
WHITE = (255, 255, 255)