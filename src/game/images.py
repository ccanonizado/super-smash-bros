'''

This file contains all the images!

Find the correct label if you want to add or modify values.
If the label does not exist for your new value, just create a new one.

'''

import pygame as pg
import os
os.chdir('..')

# other backgrounds
INTRO_BG = pg.image.load('./images/backgrounds/intro.png')
ABOUT_BG = pg.image.load('./images/backgrounds/about.png')
GUIDE_BG = pg.image.load('./images/backgrounds/guide.png')
ARENA_BG = pg.image.load('./images/backgrounds/arena.png')
CHAT_BG = pg.image.load('./images/backgrounds/chat.png')

# start section backgrounds
START_NAME_BG = pg.image.load('./images/backgrounds/startName.png')
START_NAME_EXISTS_BG = pg.image.load('./images/backgrounds/startNameExists.png')
START_NO_NAME_BG = pg.image.load('./images/backgrounds/startNoName.png')
START_CHARACTER_BG = pg.image.load('./images/backgrounds/startCharacter.png')
START_WAITING_BG = pg.image.load('./images/backgrounds/startWaiting.png')

#icon
ICON = pg.image.load('./images/others/icon.png')

'''

Character sprites:

NOTE - The images are one by one though we were supposed to use a sprite sheet.
Upon using the sprite sheet there were a lot of unnecessary frames.
Hence we just picked the ones we needed for easier indexing.

D -> damaged
S -> standing
W -> weak attack
H -> heavy attack
M -> movement

Most sprites are facing right

'''

# Dead
dead = pg.image.load('./images/characters/dead.png')

# Mario
maD1 = pg.image.load('./images/characters/mario/d1.png')
maW1 = pg.image.load('./images/characters/mario/w1.png')
maH1 = pg.image.load('./images/characters/mario/h1.png')
maS1 = pg.image.load('./images/characters/mario/s1.png')
maM1 = pg.image.load('./images/characters/mario/m1.png')
maM2 = pg.image.load('./images/characters/mario/m2.png')
maM3 = pg.image.load('./images/characters/mario/m3.png')
maM4 = pg.image.load('./images/characters/mario/m4.png')
maM5 = pg.image.load('./images/characters/mario/m5.png')
maM6 = pg.image.load('./images/characters/mario/m6.png')
maM7 = pg.image.load('./images/characters/mario/m7.png')

# Luigi
luD1 = pg.image.load('./images/characters/luigi/d1.png')
luW1 = pg.image.load('./images/characters/luigi/w1.png')
luH1 = pg.image.load('./images/characters/luigi/h1.png')
luS1 = pg.image.load('./images/characters/luigi/s1.png')
luM1 = pg.image.load('./images/characters/luigi/m1.png')
luM2 = pg.image.load('./images/characters/luigi/m2.png')
luM3 = pg.image.load('./images/characters/luigi/m3.png')
luM4 = pg.image.load('./images/characters/luigi/m4.png')
luM5 = pg.image.load('./images/characters/luigi/m5.png')
luM6 = pg.image.load('./images/characters/luigi/m6.png')
luM7 = pg.image.load('./images/characters/luigi/m7.png')
luM8 = pg.image.load('./images/characters/luigi/m8.png')

# Yoshi
yoD1 = pg.image.load('./images/characters/yoshi/d1.png')
yoW1 = pg.image.load('./images/characters/yoshi/w1.png')
yoH1 = pg.image.load('./images/characters/yoshi/h1.png')
yoS1 = pg.image.load('./images/characters/yoshi/s1.png')
yoM1 = pg.image.load('./images/characters/yoshi/m1.png')
yoM2 = pg.image.load('./images/characters/yoshi/m2.png')
yoM3 = pg.image.load('./images/characters/yoshi/m3.png')
yoM4 = pg.image.load('./images/characters/yoshi/m4.png')
yoM5 = pg.image.load('./images/characters/yoshi/m5.png')
yoM6 = pg.image.load('./images/characters/yoshi/m6.png')
yoM7 = pg.image.load('./images/characters/yoshi/m7.png')
yoM8 = pg.image.load('./images/characters/yoshi/m8.png')

# Popo (facing left)
poD1 = pg.image.load('./images/characters/popo/d1.png')
poW1 = pg.image.load('./images/characters/popo/w1.png')
poH1 = pg.image.load('./images/characters/popo/h1.png')
poS1 = pg.image.load('./images/characters/popo/s1.png')
poM1 = pg.image.load('./images/characters/popo/m1.png')
poM2 = pg.image.load('./images/characters/popo/m2.png')
poM3 = pg.image.load('./images/characters/popo/m3.png')

# Nana (facing left)
naD1 = pg.image.load('./images/characters/nana/d1.png')
naW1 = pg.image.load('./images/characters/nana/w1.png')
naH1 = pg.image.load('./images/characters/nana/h1.png')
naS1 = pg.image.load('./images/characters/nana/s1.png')
naM1 = pg.image.load('./images/characters/nana/m1.png')
naM2 = pg.image.load('./images/characters/nana/m2.png')
naM3 = pg.image.load('./images/characters/nana/m3.png')

# Link
liD1 = pg.image.load('./images/characters/link/d1.png')
liW1 = pg.image.load('./images/characters/link/w1.png')
liH1 = pg.image.load('./images/characters/link/h1.png')
liS1 = pg.image.load('./images/characters/link/s1.png')
liM1 = pg.image.load('./images/characters/link/m1.png')
liM2 = pg.image.load('./images/characters/link/m2.png')
liM3 = pg.image.load('./images/characters/link/m3.png')
liM4 = pg.image.load('./images/characters/link/m4.png')
liM5 = pg.image.load('./images/characters/link/m5.png')
liM6 = pg.image.load('./images/characters/link/m6.png')
liM7 = pg.image.load('./images/characters/link/m7.png')
liM8 = pg.image.load('./images/characters/link/m8.png')
liM9 = pg.image.load('./images/characters/link/m9.png')
liM10 = pg.image.load('./images/characters/link/m10.png')
