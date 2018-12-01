'''

This is the main game file!

All the other classes are distributed in the different directories:
- /src/game/characters/ - Player.py and all other Character.pys
- /src/game/objects/ - Base.py, Button.py, and Platform.py

Other classes used in this directory are:
- Chat.py for the multiplayer chat using TCP
- settings.py for all the configurations needed

For ease of navigation search the following labels:
"IMPORTANT METHODS" - game events and updates
"SCREENS" - different game menus

'''

from objects.Button import Button
from objects.CharButton import CharButton
from objects.ReadyButton import ReadyButton
from objects.Platform import Platform
from characters.Player import Player
from settings import *
from images import *
from Chat import Chat
import pygame as pg

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
        self.status = INTRO
        self.running = True

        # converted backgrounds for optimized game loop
        self.arena_bg = ARENA_BG.convert()
        self.chat_bg = CHAT_BG.convert()

        # chat variables
        self.chat_text = ''
        self.chatting = False
        self.chat_once = False
        self.chat_init = False
        self.chat_messages = []

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

        self.player = Player(self, [100,0])
        self.all_sprites.add(self.player)

        base = Platform('floor', 0, HEIGHT-30, GAME_WIDTH, 30)
        self.all_sprites.add(base)
        self.platforms.add(base)

        plat1 = Platform('platform', 60, 460, 200, 50)
        self.all_sprites.add(plat1)
        self.platforms.add(plat1)

        plat2 = Platform('platform', 435, 460, 200, 50)
        self.all_sprites.add(plat2)
        self.platforms.add(plat2)

        plat3 = Platform('platform', 250, 260, 200, 50)
        self.all_sprites.add(plat3)
        self.platforms.add(plat3)

        self.run()


    def events(self):
        keys = pg.key.get_pressed()

        # once player enters game screen - show initial chat
        if not self.chat_init:
            self.chat_text = '<Enter> disables movement!'
            self.chat_init = True

        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            # majority of chat flow
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if not self.chatting:
                        self.chatting = True

                        # first enter will replace default text
                        self.chat_once = True
                        self.chat_text = 'Type here!'

                    elif self.chatting:
                        self.chatting = False

                        # send message to server and replace with default text
                        self.chat.chatInLobby(self.chat_text)
                        self.chat_text = '<Enter> disables movement!'

                elif event.key == pg.K_BACKSPACE:
                   
                    # self.chat_once just clears 'Type here!' after initial type
                    if self.chatting:
                        if self.chat_once:
                            self.chat_once = False
                            self.chat_text = ''
                        else:
                            self.chat_text = self.chat_text[:-1]
                else:
                    if self.chatting:
                        if self.chat_once:
                            self.chat_once = False
                            self.chat_text = ''
                        
                        # maximum message length is 22 to fit the screen
                        if len(self.chat_text) <= 22:
                            char = event.unicode
                            self.chat_text += char

    def update(self):
        self.all_sprites.update()

        if self.player.vel.y > 0:
            collision = pg.sprite.spritecollide(self.player, self.platforms, False)
            if collision:
                self.player.pos.y = collision[0].rect.top + 1
                self.player.vel.y = 0

    # for consistently drawing the background and the sprites
    def draw(self):
        self.screen.blit(self.arena_bg, ORIGIN)
        self.screen.blit(self.chat_bg, (700,0))
        self.all_sprites.draw(self.screen)

        # show the input chat
        font = pg.font.Font(None, 30)
        text_surface = font.render(self.chat_text, True, WHITE)
        self.screen.blit(text_surface, (760,644))

        # show all the messages
        font2 = pg.font.Font(None, 24)
        for i in range(0,len(self.chat_messages)):
            text_surface2 = font2.render(self.chat_messages[i], True, BLACK)
            self.screen.blit(text_surface2, (730,95+(i*25)))

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
                    quit()
                
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

            self.screen.blit(start.image, (start.x, start.y))
            self.screen.blit(guide.image, (guide.x, guide.y))
            self.screen.blit(about.image, (about.x, about.y))

            pg.display.flip()

    # guide or about menu
    def other_menu(self, flag, bg):
        back = Button('back', 20, 20, 100, 100)

        while self.status == flag:
            self.screen.blit(bg, ORIGIN)

            for event in pg.event.get():
                pos = pg.mouse.get_pos()

                if event.type == pg.QUIT:
                    quit()
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if back.isOver(pos):
                        self.status = INTRO
                        break

                if event.type == pg.MOUSEMOTION:
                    back.isOver(pos)

            self.screen.blit(back.image, (back.x, back.y))

            pg.display.flip()

    # this menu includes the name input - character select - ready screen
    def start_menu(self):
        back = Button('back', 20, 20, 100, 100)
        ready = ReadyButton('ready', 400, 560, 300, 100)
        mario = CharButton('mario', 25, 210, 150, 350)
        luigi = CharButton('luigi', 210, 210, 150, 350)
        yoshi = CharButton('yoshi', 390, 210, 150, 350)
        popo = CharButton('popo', 575, 210, 150, 350)
        nana = CharButton('nana', 750, 210, 150, 350)
        link = CharButton('link', 920, 210, 150, 350)

        font = pg.font.Font(None, 100)
        character = 10
        screen = 'name'
        players = 0
        text = ''

        while self.status == START:
            if screen == 'name':
                self.screen.blit(START_NAME_BG, ORIGIN)
            elif screen == 'no_name':
                self.screen.blit(START_NO_NAME_BG, ORIGIN)
            elif screen == 'character':
                self.screen.blit(START_CHARACTER_BG, ORIGIN)
            elif screen == 'waiting':
                self.screen.blit(START_WAITING_BG, ORIGIN)

            if screen == 'name' or screen == 'no_name':
                text_surface = font.render(text, True, WHITE)
                self.screen.blit(text_surface, (355,355))
            elif screen == 'waiting':
                text_surface = font.render(str(players), True, WHITE)
                self.screen.blit(text_surface,(700,440))
            
            for event in pg.event.get():
                pos = pg.mouse.get_pos()

                if event.type == pg.QUIT:
                    quit()
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if back.isOver(pos):
                        if screen == 'name':
                            self.status = INTRO
                            break
                        elif screen == 'no_name':
                            self.status = INTRO
                            break
                        elif screen == 'character':
                            screen = 'name'
                        elif screen == 'waiting':
                            screen = 'character'
                    if screen == 'character':
                        if mario.isOver(pos, 'mario'):
                            character = MARIO
                            screen = 'waiting'
                        elif luigi.isOver(pos, 'luigi'):
                            character = LUIGI
                            screen = 'waiting'
                        elif yoshi.isOver(pos, 'yoshi'):
                            character = YOSHI
                            screen = 'waiting'
                        elif popo.isOver(pos, 'popo'):
                            character = POPO
                            screen = 'waiting'
                        elif nana.isOver(pos, 'nana'):
                            character = NANA
                            screen = 'waiting'
                        elif link.isOver(pos, 'link'):
                            character = LINK
                            screen = 'waiting'
                    if screen == 'waiting':
                        if ready.isOver(pos):
                            if ready.clicked:
                                players -= 1
                                ready.click()
                            else:
                                players += 1
                                ready.click()

                if event.type == pg.MOUSEMOTION:
                    back.isOver(pos)
                    if screen == 'character':
                        mario.isOver(pos, 'mario')
                        luigi.isOver(pos, 'luigi')
                        yoshi.isOver(pos, 'yoshi')
                        popo.isOver(pos, 'popo')
                        nana.isOver(pos, 'nana')
                        link.isOver(pos, 'link')
                    if screen == 'waiting':
                        ready.isOver(pos)

                if event.type == pg.KEYDOWN:
                    if screen == 'name' or screen == 'no_name':
                        if event.key == pg.K_RETURN:
                            if len(text) == 0:
                                screen = 'no_name'
                            else:
                                screen = 'character'
                        elif event.key == pg.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            # limit character length for the screen
                            if len(text) < 10:
                                char = event.unicode
                                text += char
            
            if screen == 'character':
                self.screen.blit(mario.image, (mario.x, mario.y))
                self.screen.blit(luigi.image, (luigi.x, luigi.y))
                self.screen.blit(yoshi.image, (yoshi.x, yoshi.y))
                self.screen.blit(popo.image, (popo.x, popo.y))
                self.screen.blit(nana.image, (nana.x, nana.y))
                self.screen.blit(link.image, (link.x, link.y))
            elif screen == 'waiting':
                self.screen.blit(ready.image, (ready.x, ready.y))

            self.screen.blit(back.image, (back.x, back.y))

            pg.display.flip()
        
# main start of the program
game = Game()

while game.running:
    game.new()

pg.quit()