from objects.Button import Button
import pygame as pg
from settings import *
# from sprites import *

START_BG = pg.image.load('./images/backgrounds/start.png')
ARENA_BG = pg.image.load('./images/backgrounds/arena.png')
CHAT_BG = pg.image.load('./images/backgrounds/chat.png')

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
        self.status = START

    def run(self):
        self.playing = True

        if self.status == START:
            self.start_menu()

        # main game loop (fighting)
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            # self.draw()
            
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

    # def draw(self):
    #     self.screen.fill(BLACK)
    #     self.all_sprites.draw(self.screen)
    #     pg.display.flip()

    # ========================= SCREENS =========================

    def start_menu(self):
        start = Button('start', 400, 275, 300, 100)
        guide = Button('guide', 400, 400, 300, 100)
        about = Button('about', 400, 525, 300, 100)

        while True:
            self.screen.blit(START_BG, ORIGIN)

            for event in pg.event.get():
                pos = pg.mouse.get_pos()

                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if start.isOver(pos):
                        print("Clicked Start")
                    if guide.isOver(pos):
                        print("Clicked Guide")
                    if about.isOver(pos):
                        print("Clicked About")

                if event.type == pg.MOUSEMOTION:
                    # change the button image
                    start.isOver(pos)
                    guide.isOver(pos)
                    about.isOver(pos)

            self.screen.blit(start.img, (start.x, start.y))
            self.screen.blit(guide.img, (guide.x, guide.y))
            self.screen.blit(about.img, (about.x, about.y))

            pg.display.flip()
        
# main start of the program
game = Game()
game.start_menu()

while game.running:
    game.new()
    # game.gameover()

pg.quit()


