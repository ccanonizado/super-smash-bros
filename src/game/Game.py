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
"OTHERS" - other methods such as sending to the server

Check Server.py for proper usage of the API!

'''

import sys
# check if user added an ip address argument first
if len(sys.argv) == 1:
    print('Proper usage: python/python3 Game.py <ip_address_of_server>')
    print('Type "ifconfig" in the terminal of the server to know its ip address.')
    quit()

print('!!! Make sure a server is running before playing - check Server.py!!!')
print()
print('========== SUPER SMASH BROS - Canonizado, Semilla, Serrano ==========')
print('=== If at any time - the game crashes - check the Server terminal ===')
print('Happy playing! This is the current version and limitations:')
print('- Once you create a game and enter, you must reset for a new one.')
print('- No option to recreate a game or returning to the menu menu.')
print('- Game is just an endless loop that detects winner of each round.')
print()

from objects.Button import Button
from objects.CharButton import CharButton
from objects.ReadyButton import ReadyButton
from objects.Platform import Platform
from characters.Player import Player
from threading import Thread
from settings import *
from images import *
from Chat import Chat
import pygame as pg
import socket
import json

print()
print('UPDATES (errors will show up here if ever):')

# server parameters
HOST = sys.argv[1]
PORT = 10000
BUFFER = 1024
SERVER = (HOST, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
        self.running = True # game is running
        self.initialized = False # initialized game in arena (with players)
        self.created_chat = False 
        self.player_count = 0
        self.name_available = True
        self.curr_player = ''

        # converted backgrounds for optimized game loop
        self.arena_bg = ARENA_BG.convert()
        self.chat_bg = CHAT_BG.convert()

        # chat variables
        self.chat_text = ''
        self.chatting = False
        self.chat_once = False
        self.chat_init = False
        self.chat_messages = []

        # socket to UDP server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # multiple threads for the game and chat (chat is in join game)
        self.game_thread = Thread(target=self.receive)
        self.game_thread.daemon = True
        self.game_thread.start()

    def run(self):
        self.playing = True

        # check for the current menu depending on the status
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
                # once initialized - continuously update players
                if self.initialized:
                    self.updatePlayer()
                    self.updateAllPlayers()
                self.clock.tick(FPS)
                self.events()
                self.update()
                self.draw()
            
    def new(self):
        # the players will be added after starting the game
        # see startGame() below

        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()

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
                self.running = False
                if self.playing:
                    self.playing = False
                quit()

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
                        try:
                            self.chat.chatInLobby(self.chat_text)
                        except:
                            self.chat_messages.append('CHAT ERROR! Server might be down!')
                            print('CHAT ERROR! Server might be down!')
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

        for player in self.players.values():
            if player.vel.y > 0:
                collision = pg.sprite.spritecollide(player, self.platforms, False)
                if collision:
                    player.pos.y = collision[0].rect.top + 1
                    player.vel.y = 0

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
                    self.running = False
                    if self.playing:
                        self.playing = False
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
                    self.running = False
                    if self.playing:
                        self.playing = False
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
        font2 = pg.font.Font(None, 40)
        screen = 'name'

        old_name = ''
        enteredName = False
        playerReady = False

        while self.status == START:

            # repeatedly check if the name is available
            self.checkName(self.curr_player)

            if screen == 'name':
                self.screen.blit(START_NAME_BG, ORIGIN)
            elif screen == 'no_name':
                self.screen.blit(START_NO_NAME_BG, ORIGIN)
            elif screen == 'character':
                self.screen.blit(START_CHARACTER_BG, ORIGIN)
            elif screen == 'waiting':
                self.screen.blit(START_WAITING_BG, ORIGIN)

            if screen == 'name' or screen == 'no_name':
                text_surface = font.render(self.curr_player, True, WHITE)
                self.screen.blit(text_surface, (355,355))

                if not self.name_available:
                    if self.curr_player != old_name: 
                        error = 'Name exists - try a new one!'
                        text_surface = font2.render(error, True, WHITE)
                        self.screen.blit(text_surface, (360,430))
            
            for event in pg.event.get():
                pos = pg.mouse.get_pos()

                if event.type == pg.QUIT:
                    self.running = False
                    if self.playing:
                        self.playing = False
                    if enteredName:
                        self.disconnectPlayer(self.curr_player)
                    quit()
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if back.isOver(pos) and not playerReady: 
                        if screen == 'name':
                            self.status = INTRO
                            if enteredName:
                                self.disconnectPlayer(self.curr_player)
                            break
                        elif screen == 'no_name':
                            self.status = INTRO
                            if enteredName:
                                self.disconnectPlayer(self.curr_player)
                            break
                        elif screen == 'character':
                            screen = 'name'
                        elif screen == 'waiting':
                            screen = 'character'

                    if screen == 'character':
                        if mario.isOver(pos, 'mario'):
                            self.editPlayerCharacter(self.curr_player, MARIO)
                            screen = 'waiting'
                        elif luigi.isOver(pos, 'luigi'):
                            self.editPlayerCharacter(self.curr_player, LUIGI)
                            screen = 'waiting'
                        elif yoshi.isOver(pos, 'yoshi'):
                            self.editPlayerCharacter(self.curr_player, YOSHI)
                            screen = 'waiting'
                        elif popo.isOver(pos, 'popo'):
                            self.editPlayerCharacter(self.curr_player, POPO)
                            screen = 'waiting'
                        elif nana.isOver(pos, 'nana'):
                            self.editPlayerCharacter(self.curr_player, NANA)
                            screen = 'waiting'
                        elif link.isOver(pos, 'link'):
                            self.editPlayerCharacter(self.curr_player, LINK)
                            screen = 'waiting'

                    if screen == 'waiting':
                        if ready.isOver(pos):
                            if ready.clicked:
                                self.editPlayerStatus(self.curr_player, 'unready')
                                playerReady = False
                                ready.click()
                            else:
                                self.editPlayerStatus(self.curr_player, 'ready')
                                playerReady = True
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
                    if screen == 'name' or screen == 'no_name' or screen == 'waiting':
                        if event.key == pg.K_RETURN:
                            if screen != 'waiting':
                                if len(self.curr_player) == 0:
                                    screen = 'no_name'
                                    print("INVALID NAME! Your name cannot be blank!")
                                else:
                                    if self.name_available or self.curr_player == old_name:
                                        screen = 'character'
                                        if not enteredName:
                                            enteredName = True
                                            old_name = self.curr_player
                                            self.connectPlayer(self.curr_player)
                                        elif enteredName:
                                            self.editPlayerName(old_name, self.curr_player)
                                            old_name = self.curr_player
                                    elif not self.name_available:
                                        print("NAME EXISTS! Enter a unique one!")
                            else:
                                # initialize chat to create lobby
                                self.chat = Chat(self)
                                lobby_id = self.chat.createLobby(6).lobby_id
                                self.createChatLobby(lobby_id)

                                self.startGame()

                        elif event.key == pg.K_BACKSPACE:
                            self.curr_player = self.curr_player[:-1]
                        else:
                            # limit character length for the screen
                            if len(self.curr_player) < 10:
                                char = event.unicode
                                self.curr_player += char

            if screen == 'character':
                self.screen.blit(mario.image, (mario.x, mario.y))
                self.screen.blit(luigi.image, (luigi.x, luigi.y))
                self.screen.blit(yoshi.image, (yoshi.x, yoshi.y))
                self.screen.blit(popo.image, (popo.x, popo.y))
                self.screen.blit(nana.image, (nana.x, nana.y))
                self.screen.blit(link.image, (link.x, link.y))

            elif screen == 'waiting':
                self.getPlayersReadyCount()
                self.screen.blit(ready.image, (ready.x, ready.y))
                text_surface = font.render(str(self.player_count), True, WHITE)
                self.screen.blit(text_surface,(700,440))
                self.joinGame()

            if not playerReady:
                self.screen.blit(back.image, (back.x, back.y))

            pg.display.flip()

    # ========================= OTHERS =========================
    def receive(self):
        while self.running:
            data, address = self.s.recvfrom(BUFFER)

            # if there is data
            if data:
                message = data.decode().split()
                action = message[0]

                # update player count
                if action == 'PLAYERS_READY':
                    self.player_count = int(message[1])

                # check name availability
                if action == 'CHECK_NAME':
                    if message[1] == 'taken':
                        self.name_available = False
                    elif message[1] == 'free':
                        self.name_available = True

                # instantiate all the players in the arena
                elif action == 'START_GAME':
                    if not self.initialized:
                        message.pop(0)
                        message = ' '.join(message)
                        data = json.loads(message)

                        self.players = {}
                        for key, value in data.items():
                            n = key
                            x = float(value['xPos'])
                            y = float(value['yPos'])
                            d = value['direc']
                            h = int(value['health'])
                            w = int(value['walk_c'])
                            m = value['move']
                            pos = [x, y]
                            player = Player(self, self.curr_player, n, 'alive', h, pos, d, w, m)
                            self.players[n] = player
                            self.all_sprites.add(player)
                        self.initialized = True

                # check if game has started - if it has started - join
                elif action == 'JOIN_GAME':
                    if int(message[1]) == GAME:
                        self.startGame()
                        self.status = GAME                        
                        self.joinChatLobby()

                elif action == 'JOIN_CHAT':
                    if not self.created_chat:
                        self.chat = Chat(self)
                        try:
                            self.chat.connectToLobby(message[1], self.curr_player)
                            self.chat_messages.append('You are in game {}!'.format(message[1]))
                            self.chat_thread = Thread(target=self.chat.receiveMessages)
                            self.chat_thread.daemon = True
                            self.chat_thread.start()
                        except:
                            self.chat_messages.append('CHAT ERROR! Server might be down!')
                            print('CHAT ERROR! Server might be down!')
                        self.created_chat = True

                elif action == 'UPDATE_ALL_PLAYERS':
                    message.pop(0)
                    message = ' '.join(message)
                    data = json.loads(message)
                    
                    for player in self.players.values():
                        name = player.name
                        status = data[name]['status']
                        health = int(data[name]['health'])
                        xPos = float(data[name]['xPos'])
                        yPos = float(data[name]['yPos'])
                        direc = data[name]['direc']
                        walk_c = int(data[name]['walk_c'])
                        move = data[name]['move']

                        player.status = status
                        player.health = health
                        player.pos = [xPos, yPos]
                        player.direc = direc
                        player.walk_c = walk_c
                        player.move = move

    def send(self, message):
        self.s.sendto(str.encode(message), SERVER)
    
    def connectPlayer(self, name):
        message = 'CONNECT '
        message += name
        self.send(message)

    def disconnectPlayer(self, name):
        message = 'DISCONNECT '
        message += name
        self.send(message)

    def checkName(self, name):
        message = 'CHECK_NAME '
        message += name
        self.send(message)

    def editPlayerName(self, old_name, new_name):
        message = 'EDIT_NAME '
        message += old_name + ' ' + new_name
        self.send(message)

    def editPlayerCharacter(self, name, character):
        message = 'EDIT_CHARACTER '
        message += name + ' ' + character
        self.send(message)

    def editPlayerStatus(self, name, status):
        message = 'EDIT_STATUS '
        message += name + ' ' + status
        self.send(message)

    def getPlayersReadyCount(self):
        message = 'PLAYERS_READY'
        self.send(message)

    def startGame(self):
        message = 'START_GAME'
        self.send(message)

    def joinGame(self):
        message = 'JOIN_GAME'
        self.send(message)

    def createChatLobby(self, lobby_id):
        message ='CREATE_CHAT '
        message += str(lobby_id)
        self.send(message)

    def joinChatLobby(self):
        message = 'JOIN_CHAT'
        self.send(message)

    def updatePlayer(self):
        message = 'UPDATE_PLAYER '
        player = self.players[self.curr_player]
        data = {
            'name': player.name,
            'status': player.status,
            'health': str(player.health),
            'xPos': str(player.pos[0]),
            'yPos': str(player.pos[1]),
            'direc': player.direc,
            'walk_c': str(player.walk_c),
            'move': player.move
        }
        message += json.dumps(data)
        self.send(message)

    def updateAllPlayers(self):
        message = 'UPDATE_ALL_PLAYERS'
        self.send(message)

# main start of the program
game = Game()

while game.running:
    game.new()

pg.quit()