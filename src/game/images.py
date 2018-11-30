'''

This file contains all the images!

Find the correct label if you want to add or modify values.
If the label does not exist for your new value, just create a new one.

'''

import pygame as pg

# other backgrounds
INTRO_BG = pg.image.load('./images/backgrounds/intro.png')
ABOUT_BG = pg.image.load('./images/backgrounds/about.png')
GUIDE_BG = pg.image.load('./images/backgrounds/guide.png')
ARENA_BG = pg.image.load('./images/backgrounds/arena.png')
CHAT_BG = pg.image.load('./images/backgrounds/chat.png')

# start section backgrounds - with error and success messages
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

'''

Character sprites:

The images are one by one though we were supposed to use a sprite sheet.
Upon using the sprite sheet there were a lot of unnecessary frames.
Hence we just picked the ones we needed for easier indexing.

s -> standing
m -> movement
w -> weak attack
h -> heavy attack

'''

# Mario
maS1 = pg.image.load('./images/characters/mario/s1.png')
maM1 = pg.image.load('./images/characters/mario/m1.png')
maM2 = pg.image.load('./images/characters/mario/m2.png')
maM3 = pg.image.load('./images/characters/mario/m3.png')
maM4 = pg.image.load('./images/characters/mario/m4.png')
maM5 = pg.image.load('./images/characters/mario/m5.png')
maM6 = pg.image.load('./images/characters/mario/m6.png')
maM7 = pg.image.load('./images/characters/mario/m7.png')
