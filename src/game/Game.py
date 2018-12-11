'''

This is the main game file!

All the other classes are distributed in the different directories:
- /src/game/characters/ - Character.pys
- /src/game/objects/ - Button.py, CharButton.py, ReadyButton.py, and Platform.py
- /src/game/menus/ - Intro.py, Other.py, and Start.py

Other classes used in this directory are:
- Server.py for the multiplayer game using UDP
- Chat.py for the multiplayer chat using TCP
- settings.py for all the configurations needed
- images.py for all the photos imported

NOTE - Check Server.py for proper usage of the API!

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
print('- No option to recreate a game or to return to the main menu.')
print('- Game is just an endless loop that detects winner of each round.')
print()

# characters
from characters.Mario import Mario
from characters.Luigi import Luigi
from characters.Yoshi import Yoshi
from characters.Popo import Popo
from characters.Nana import Nana
from characters.Link import Link

# menus
from menus.Intro import Intro
from menus.Other import Other
from menus.Start import Start

# others
from objects.Platform import Platform
from threading import Thread
from settings import *
from images import *

try:
    from Chat import Chat
except:
    print("You must install protobuf for python if you want to use the chat!")
    print()

# dependencies
import pygame as pg
import socket
import json

print()
print('UPDATES (errors will show up here if ever):')

# server parameters
HOST = sys.argv[1]
PORT = 8000
BUFFER = 4096
SERVER = (HOST, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class Game:
    # ========================= IMPORTANT METHODS =========================
    def __init__(self):

        # initialize
        pg.init()
        pg.mixer.init()
        pg.display.set_caption(TITLE)
        pg.display.set_icon(ICON)

        # game variables
        self.screen = pg.display.set_mode(BG_SIZE)
        self.clock = pg.time.Clock()
        self.status = INTRO
        self.running = True # game is running
        self.all_ready = False # checks if everyone is ready
        self.showed_end = False # checks if end game results have been showed
        self.initialized = False # initialized game in arena (with players)
        self.created_chat = False # created chat lobby for everyone to connect
        self.name_available = True # checks if curr_player text is available
        self.restart_request = False # checks if player requested for a restart
        self.curr_player = '' # value during input name screen
        self.player_count = 0 # for the ready screen

        # converted background images for optimized game loop
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
        # check for the current menu depending on the status
        while True:
            if self.status == INTRO:
                Intro(self)

            elif self.status == START:
                Start(self)

            elif self.status == GUIDE:
                Other(self, GUIDE, GUIDE_BG)

            elif self.status == ABOUT:
                Other(self, ABOUT, ABOUT_BG)

            elif self.status == GAME:
                self.winner = ''
                self.getStatus()
                # once initialized - continuously update players and check for a winner
                if self.initialized and self.playing:
                    self.checkDisconnect()
                    self.checkWinner()
                    self.updatePlayer()
                    self.updateAllPlayers()
                self.clock.tick(FPS)
                self.events()
                self.update()
                self.draw()
            
    def new(self):
        # the players will be added after starting the game
        # see startGame() below

        self.enemy_sprites = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()

        self.loadPlatforms()
        self.run()

    def loadPlatforms(self):
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

    def events(self):
        # try:
        if self.restart_request and self.showed_end:
            self.restartGame()

        keys = pg.key.get_pressed()

        # once player enters game screen - show initial chat
        if not self.chat_init:
            self.chat_text = '<Enter> disables movement!'
            self.chat_init = True

        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:                    
                print("You quit in the middle of the game!")
                self.disconnectPlayer(self.curr_player)

                if self.playing:
                    self.playing = False

                # if end game detected - quit other players as well
                if self.showed_end:
                    self.quitGame()

                self.running = False
                self.s.close()
                quit()

            # majority of chat flow + attacks
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    self.players[self.curr_player].weakAttack()

                elif event.key == pg.K_x:
                    self.players[self.curr_player].heavyAttack()

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

                elif event.key == pg.K_F1:
                    if self.showed_end:
                        if not self.restart_request:
                            self.restartRequest()
                            self.restart_request = True
                            self.chat_messages.append('You sent a restart request!')

                elif event.key == pg.K_ESCAPE:
                    if self.showed_end:
                        self.quitGame()

                else:
                    if self.chatting:
                        if self.chat_once:
                            self.chat_once = False
                            self.chat_text = ''
                        
                        # maximum message length is 22 to fit the screen
                        if len(self.chat_text) <= 22:
                            char = event.unicode
                            self.chat_text += char

        if keys[pg.K_BACKSPACE]:
            
            # self.chat_once just clears 'Type here!' after initial type
            if self.chatting:
                if self.chat_once:
                    self.chat_once = False
                    self.chat_text = ''
                else:
                    self.chat_text = self.chat_text[:-1]
    
        # except:
        #     quit()

    def update(self):
        # try:
        self.all_sprites.update()

        # check for collision with platforms
        for player in self.players.values():
            if player.vel.y > 0:
                collision = pg.sprite.spritecollide(player, self.platforms, False)
                if collision:
                    player.pos[1] = collision[0].rect.top + 1
                    player.vel[1] = 0
        
        # except:
        #     quit()

    # for consistently drawing the background and the sprites
    def draw(self):
        # try:
        # show the background
        self.screen.blit(self.arena_bg, ORIGIN)
        self.screen.blit(self.chat_bg, (700,0))
        
        # check method below
        self.drawStatsBoard()
        
        # show all the sprites
        self.all_sprites.draw(self.screen)

        # write the player's name on top of the sprite
        font = pg.font.Font(None, 20)
        for player in self.players.values():
            coors = (player.rect.left, player.rect.top-15)
            text_surface = font.render((player.name), True, WHITE)
            self.screen.blit(text_surface, coors)

        # show end game results
        if len(self.winner) > 0 and not self.showed_end:
            self.initialized = False
            self.playing = False

            self.chat_messages = []
            self.chat_messages.append('===== {} won this round! ====='.format(self.winner))
            self.chat_messages.append("-> Press F1 to restart the game")
            self.chat_messages.append('   * Everyone must press F1 to restart')
            self.chat_messages.append('-> Press Esc to exit the game')
            self.chat_messages.append('   * Recreating is not supported for now')
            self.chat_messages.append('   * If you want to recreate a game:')
            self.chat_messages.append('     Simply run Game.py <ip_address> again')
            self.chat_messages.append('! ENJOY, you may still chat !')
            self.chat_messages.append('======================================')

            self.showed_end = True

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
        
        # except:
        #     quit()

    # board with the players' name and life
    def drawStatsBoard(self):
        font = pg.font.Font(None, 22)
        text = font.render('Player - Life', True, WHITE)
        pg.draw.rect(self.screen, BLACK, (10, 10, 140, 20))
        pg.draw.rect(self.screen, GRAY, (10, 30, 140, 30*len(self.players)))
        self.screen.blit(text, (37,12))

        i = 0        
        for player in self.players.values():
            name = player.name
            stats = name + ' - ' + str(int(player.health))
            diff = 10 - len(player.name)

            # color text according to player's health
            if player.health > 60:
                text = font.render(stats, True, GREEN)
            elif player.health <= 60 and player.health > 20:
                text = font.render(stats, True, ORANGE) 
            elif player.health <= 20 and player.health > 0:
                text = font.render(stats, True, RED)
            elif player.health == 0:
                text = font.render(stats, True, BLACK)

            self.screen.blit(text, (12+(diff*5),40+(i*30)))
            i += 1

    # ========================= DATA TO AND FROM SERVER =========================
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
                            h = float(value['health'])
                            w = int(value['walk_c'])
                            m = value['move']
                            pos = [x, y]
                            char = value['character']
                            a = 'alive'

                            if char == MARIO:
                                player = Mario(self, self.curr_player, n, a, h, pos, d, w, m)
                            elif char == LUIGI:
                                player = Luigi(self, self.curr_player, n, a, h, pos, d, w, m)
                            elif char == YOSHI:
                                player = Yoshi(self, self.curr_player, n, a, h, pos, d, w, m)
                            elif char == POPO:
                                player = Popo(self, self.curr_player, n, a, h, pos, d, w, m)
                            elif char == NANA:
                                player = Nana(self, self.curr_player, n, a, h, pos, d, w, m)
                            elif char == LINK:
                                player = Link(self, self.curr_player, n, a, h, pos, d, w, m)

                            self.players[n] = player
                            self.all_sprites.add(player)
                            if self.curr_player != n:
                                self.enemy_sprites.add(player)
                        
                        self.initialized = True

                elif action == 'RESTART_GAME':
                    message.pop(0)
                    message = ' '.join(message)
                    data = json.loads(message)

                    self.players = {}
                    self.enemy_sprites = pg.sprite.Group()
                    self.all_sprites = pg.sprite.Group()
                    self.platforms = pg.sprite.Group()
                    self.loadPlatforms()
                    
                    for key, value in data.items():
                        n = key
                        x = float(value['xPos'])
                        y = float(value['yPos'])
                        d = value['direc']
                        h = float(value['health'])
                        w = int(value['walk_c'])
                        m = value['move']
                        pos = [x, y]
                        char = value['character']
                        a = 'alive'

                        if char == MARIO:
                            player = Mario(self, self.curr_player, n, a, h, pos, d, w, m)
                        elif char == LUIGI:
                            player = Luigi(self, self.curr_player, n, a, h, pos, d, w, m)
                        elif char == YOSHI:
                            player = Yoshi(self, self.curr_player, n, a, h, pos, d, w, m)
                        elif char == POPO:
                            player = Popo(self, self.curr_player, n, a, h, pos, d, w, m)
                        elif char == NANA:
                            player = Nana(self, self.curr_player, n, a, h, pos, d, w, m)
                        elif char == LINK:
                            player = Link(self, self.curr_player, n, a, h, pos, d, w, m)

                        self.players[n] = player
                        self.all_sprites.add(player)
                        if self.curr_player != n:
                            self.enemy_sprites.add(player)

                    self.chat_messages = []
                    self.chat_messages.append('=========== GAME RESTART ===========')
                    self.chat_messages.append('Best of luck - may the best player win!')
                    self.chat_messages.append('======================================')
                   
                   # reset some game variables
                    self.status = GAME
                    self.playing = True
                    self.initialized = True
                    self.showed_end = False
                    self.restart_request = False

                # check if game has started - if it has started - join
                elif action == 'JOIN_GAME':
                    if int(message[1]) == GAME:
                        self.startGame()
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

                elif action == 'CHECK_DISCONNECT':
                    if len(message) > 1:
                        if message[1] in self.players:
                            if self.playing:
                                self.all_sprites.remove(self.players[message[1]])   
                                self.enemy_sprites.remove(self.players[message[1]])
                                self.players.pop(message[1])

                elif action == 'QUIT_GAME':
                    print("Thank you for playing!")
                    self.running = False
                    self.s.close()
                    pg.quit()
                    quit()

                elif action == 'GET_STATUS':
                    if int(message[1]) == QUIT:
                        print("Thank you for playing!")
                        self.running = False
                        pg.quit()
                        quit()

                elif action == 'CHECK_WINNER':
                    self.winner = message[1]

                elif action == 'CHECK_READY':
                    if message[1] == 'TRUE':
                        self.all_ready = True
                    elif message[1] == 'FALSE':
                        self.all_ready = False

                elif action == 'UPDATE_ALL_PLAYERS':
                    message.pop(0)
                    message = ' '.join(message)
                    data = json.loads(message)
                    
                    if(len(data) != len(self.players)):
                        continue

                    for player in self.players.values():
                        name = player.name
                        status = data[name]['status']
                        health = float(data[name]['health'])
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

    # ========================= METHODS TO MAKE REQUESTS TO SERVER =========================
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

    def checkDisconnect(self):
        message = 'CHECK_DISCONNECT'
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

    def attackPlayer(self, player, damage, move):
        message = 'ATTACK_PLAYER '
        message += player + ' ' + str(damage) + ' ' + move
        self.send(message)

    def restartRequest(self):
        message = 'RESTART_REQUEST'
        self.send(message)

    def restartGame(self):
        message = 'RESTART_GAME'
        self.send(message)

    def quitGame(self):
        message = 'QUIT_GAME'
        self.send(message)

    def getStatus(self):
        message = 'GET_STATUS'
        self.send(message)     

    def checkWinner(self):
        message = 'CHECK_WINNER'
        self.send(message)      

    def checkReady(self):
        message = 'CHECK_READY'
        self.send(message)            

    # NOTE - for the full API of the requests - please refer to Server.py                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

# main start of the program
game = Game()

while game.running:
    game.new()