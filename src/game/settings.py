import pygame as pg

# game values
TITLE = "Super Smash Bros"
BG_SIZE = (1100, 700) 
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
START1_BG = pg.image.load('./images/backgrounds/start1.png')
START2A_BG = pg.image.load('./images/backgrounds/start2a.png')
START2B_BG = pg.image.load('./images/backgrounds/start2b.png')
ABOUT_BG = pg.image.load('./images/backgrounds/about.png')
GUIDE_BG = pg.image.load('./images/backgrounds/guide.png')
ARENA_BG = pg.image.load('./images/backgrounds/arena.png')
CHAT_BG = pg.image.load('./images/backgrounds/chat.png')