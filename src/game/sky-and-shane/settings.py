import random 
import os

TITLE = "Test"
WIDTH = 700
HEIGHT = 700
FPS = 60

ACC = 0.5
FRIC = -0.12
VEL = 15

BLUE = (59,148,238)
BLACK = (0,0,0)
BROWN = (45, 33, 19)


game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")