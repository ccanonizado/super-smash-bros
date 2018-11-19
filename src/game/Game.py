import pygame as pg
from settings import *
# from sprites import *

START_BG = pg.image.load(BACKGROUNDS+'./start.png')
ARENA_BG = pg.image.load(BACKGROUNDS+'./arena.png')
CHAT_BG = pg.image.load(BACKGROUNDS+'./chat.png')

class Game:
    # ========================= IMPORTANT METHODS =========================
    def __init__(self):

        # initialize
        pg.init()
        pg.mixer.init()
        pg.display.set_caption(TITLE)

        # game variables
        self.screen = pg.display.set_mode(BG_SIZE)
        self.clock = pg.time.Clock()
        self.running = True

    def run(self):
        self.start_menu()
        self.playing = True

        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def new(self):

        # sprite groups for later use
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        # self.player = Player(self)

        self.run()

    def events(self):
        keys = pg.key.get_pressed()

        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    # ========================= SCREENS =========================

    def start_menu(self):
        self.screen.blit(START_BG, ORIGIN)
        pg.display.flip()
        while True:
            print("Hello")

        
# main start of the program
game = Game()
game.start_menu()

while game.running:
    game.new()
    # game.gameover()

pg.quit()


