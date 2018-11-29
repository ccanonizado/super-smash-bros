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

# characters
MARIO = pg.image.load('./characters/mario/2.png')