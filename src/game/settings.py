'''

This file contains all the settings!

Find the correct label if you want to add or modify values.
If the label does not exist for your new value, just create a new one.

You can also find all the background images here.

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

# background images
INTRO_BG = pg.image.load('./images/backgrounds/intro.png')
ABOUT_BG = pg.image.load('./images/backgrounds/about.png')
GUIDE_BG = pg.image.load('./images/backgrounds/guide.png')
ARENA_BG = pg.image.load('./images/backgrounds/arena.png')
CHAT_BG = pg.image.load('./images/backgrounds/chat.png')

# start section - with error images
START1_BG = pg.image.load('./images/backgrounds/start1.png')
START2A_BG = pg.image.load('./images/backgrounds/start2a.png')
START2A_FAIL_BG = pg.image.load('./images/backgrounds/start2aFail.png')
START2A_SUCCESS_BG = pg.image.load('./images/backgrounds/start2aSuccess.png')
START2B_DNE_BG = pg.image.load('./images/backgrounds/start2bDNE.png')
START2B_FOUND_BG = pg.image.load('./images/backgrounds/start2bFound.png')
START2B_LOBBY_BG = pg.image.load('./images/backgrounds/start2bLobby.png')
START2B_NAME_BG = pg.image.load('./images/backgrounds/start2bName.png')
START2B_NO_NAME_BG = pg.image.load('./images/backgrounds/start2bNoName.png')
START2B_FULL_BG = pg.image.load('./images/backgrounds/start2bFull.png')