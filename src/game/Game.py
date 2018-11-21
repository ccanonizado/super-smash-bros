from objects.Button import Button
from settings import *
import pygame as pg
# from sprites import *

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
        self.status = INTRO

    def run(self):
        self.playing = True

        while self.playing:
            if self.status == INTRO:
                self.intro_menu()

            elif self.status == START:
                self.start_menu()

            elif self.status == GUIDE:
                self.other_menu(GUIDE, GUIDE_BG)

            elif self.status == ABOUT:
                self.other_menu(ABOUT, ABOUT_BG)

            elif self.status == GAME:
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
        self.screen.blit(ARENA_BG, ORIGIN)
        self.screen.blit(CHAT_BG, (700,0))
        # self.all_sprites.draw(self.screen)
        pg.display.flip()

    # ========================= SCREENS =========================

    def intro_menu(self):
        start = Button('start', 400, 275, 300, 100)
        guide = Button('guide', 400, 400, 300, 100)
        about = Button('about', 400, 525, 300, 100)

        while self.status == INTRO:
            self.screen.blit(INTRO_BG, ORIGIN)

            for event in pg.event.get():
                pos = pg.mouse.get_pos()

                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if start.isOver(pos):
                        self.status = START
                        break
                    elif guide.isOver(pos):
                        self.status = GUIDE
                        break
                    elif about.isOver(pos):
                        self.status = ABOUT
                        break

                if event.type == pg.MOUSEMOTION:
                    start.isOver(pos)
                    guide.isOver(pos)
                    about.isOver(pos)

            self.screen.blit(start.img, (start.x, start.y))
            self.screen.blit(guide.img, (guide.x, guide.y))
            self.screen.blit(about.img, (about.x, about.y))

            pg.display.flip()

    # guide or about menu
    def other_menu(self, flag, bg):
        back = Button('back', 20, 20, 100, 100)

        while self.status == flag:
            self.screen.blit(bg, ORIGIN)

            for event in pg.event.get():
                pos = pg.mouse.get_pos()

                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if back.isOver(pos):
                        self.status = INTRO
                        break

                if event.type == pg.MOUSEMOTION:
                    back.isOver(pos)

            self.screen.blit(back.img, (back.x, back.y))

            pg.display.flip()

    def start_menu(self):
        create = Button('create', 400, 275, 300, 100)
        join = Button('join', 400, 400, 300, 100)
        back = Button('back', 20, 20, 100, 100)
        choice = 'none'
        
        font = pg.font.Font(None, 100)
        text = ''

        while self.status == START:

            if choice == 'none':
                self.screen.blit(START1_BG, ORIGIN)
            elif choice == 'create':
                self.screen.blit(START2A_BG, ORIGIN)
            elif choice == 'join':
                self.screen.blit(START2B_BG, ORIGIN)

            text_surface = font.render(text, True, WHITE)
            self.screen.blit(text_surface, (355,355))
            
            for event in pg.event.get():
                pos = pg.mouse.get_pos()

                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if create.isOver(pos):
                        choice = 'create'
                        break
                    elif join.isOver(pos):
                        choice = 'join'
                        break
                    elif back.isOver(pos):
                        if choice == 'none':
                            self.status = INTRO
                        elif choice == 'create' or choice == 'join':
                            choice = 'none'
                            text = ''
                        break

                if event.type == pg.MOUSEMOTION:
                    create.isOver(pos)
                    join.isOver(pos)
                    back.isOver(pos)

                if event.type == pg.KEYDOWN and (choice == 'create' or choice == 'join'):
                    if event.key == pg.K_RETURN:
                        text = ''
                        self.status = GAME
                        break
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        # limit character length for the screen
                        if len(text) < 10:
                            char = event.unicode
                            # validation - max players should be a number only
                            if choice == 'create':
                                if char.isdigit():
                                    text += char
                            else:
                                text += char

            if choice == 'none':
                self.screen.blit(create.img, (create.x, create.y))
                self.screen.blit(join.img, (join.x, join.y))
            
            self.screen.blit(back.img, (back.x, back.y))

            pg.display.flip()
        
# main start of the program
game = Game()

while game.running:
    game.new()
    # game.gameover()

pg.quit()


