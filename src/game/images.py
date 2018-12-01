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

# start section backgrounds
START_NAME_BG = pg.image.load('./images/backgrounds/startName.png')
START_NO_NAME_BG = pg.image.load('./images/backgrounds/startNoName.png')
START_CHARACTER_BG = pg.image.load('./images/backgrounds/startCharacter.png')
START_WAITING_BG = pg.image.load('./images/backgrounds/startWaiting.png')

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
