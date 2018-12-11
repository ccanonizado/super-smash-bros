import sys
import pygame as pg

# move up one directory to be able to import the settings and images
sys.path.append("..")
from objects.Button import Button
from objects.CharButton import CharButton
from objects.ReadyButton import ReadyButton
from settings import *
from images import *
from Chat import Chat

class Start:
    def __init__(self, game):
        self.g = game

        back = Button('back', 20, 20, 100, 100)
        ready = ReadyButton('ready', 400, 560, 300, 100)
        mario = CharButton('mario', 25, 210, 150, 350)
        luigi = CharButton('luigi', 210, 210, 150, 350)
        yoshi = CharButton('yoshi', 390, 210, 150, 350)
        popo = CharButton('popo', 575, 210, 150, 350)
        nana = CharButton('nana', 750, 210, 150, 350)
        link = CharButton('link', 920, 210, 150, 350)

        '''

        NOTE - screen is the current background

        name = input for player's name
        no_name = no player input for name
        character = character selection
        waiting = ready / unready screen

        '''

        screen = 'name'

        old_name = ''
        enteredName = False
        player_ready = False

        font = pg.font.Font(None, 100)

        # note - self.g.curr_player = current text of the input player name

        while self.g.status == START:

            if screen == 'name' or screen == 'no_name':
                self.g.checkName(self.g.curr_player)

            if screen == 'name':
                self.g.screen.blit(START_NAME_BG, ORIGIN)
            elif screen == 'no_name':
                self.g.screen.blit(START_NO_NAME_BG, ORIGIN)
            elif screen == 'character':
                self.g.screen.blit(START_CHARACTER_BG, ORIGIN)
                self.drawStats()
            elif screen == 'waiting':
                self.g.screen.blit(START_WAITING_BG, ORIGIN)
                self.g.getPlayersReadyCount()
                text_surface = font.render(str(self.g.player_count), True, WHITE)
                self.g.screen.blit(text_surface,(700,445))
                
                self.g.checkReady()
                self.g.joinGame()

            if screen == 'name' or screen == 'no_name':
                if not self.g.name_available:
                    # allow changing the name to player's own name
                    # even though technically - that name is taken
                    if self.g.curr_player != old_name: 
                        self.g.screen.blit(START_NAME_EXISTS_BG, ORIGIN)

                text_surface = font.render(self.g.curr_player, True, WHITE)
                self.g.screen.blit(text_surface, (355,355))
            
            for event in pg.event.get():
                pos = pg.mouse.get_pos()

                if event.type == pg.QUIT:
                    print("You quit in the middle of the game!")
                    if enteredName:
                        self.g.disconnectPlayer(self.g.curr_player)
                    self.g.running = False
                    self.g.s.close()
                    quit()
                
                # mouse click
                if event.type == pg.MOUSEBUTTONDOWN:
                    if back.isOver(pos) and not player_ready: 
                        if screen == 'name':
                            self.g.status = INTRO
                            if enteredName:
                                self.g.disconnectPlayer(self.g.curr_player)
                        elif screen == 'no_name':
                            self.g.status = INTRO
                            if enteredName:
                                self.g.disconnectPlayer(self.g.curr_player)
                        elif screen == 'character':
                            screen = 'name'
                        elif screen == 'waiting':
                            screen = 'character'

                    if screen == 'character':
                        if mario.isOver(pos, 'mario'):
                            self.g.editPlayerCharacter(self.g.curr_player, MARIO)
                            screen = 'waiting'
                        elif luigi.isOver(pos, 'luigi'):
                            self.g.editPlayerCharacter(self.g.curr_player, LUIGI)
                            screen = 'waiting'
                        elif yoshi.isOver(pos, 'yoshi'):
                            self.g.editPlayerCharacter(self.g.curr_player, YOSHI)
                            screen = 'waiting'
                        elif popo.isOver(pos, 'popo'):
                            self.g.editPlayerCharacter(self.g.curr_player, POPO)
                            screen = 'waiting'
                        elif nana.isOver(pos, 'nana'):
                            self.g.editPlayerCharacter(self.g.curr_player, NANA)
                            screen = 'waiting'
                        elif link.isOver(pos, 'link'):
                            self.g.editPlayerCharacter(self.g.curr_player, LINK)
                            screen = 'waiting'

                    if screen == 'waiting':
                        if not player_ready:
                            if ready.isOver(pos):
                                self.g.editPlayerStatus(self.g.curr_player, 'ready')
                                player_ready = True
                                ready.click()

                # mouse hover
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
                        if not player_ready:
                            ready.isOver(pos)

                if event.type == pg.KEYDOWN:
                    if screen == 'name' or screen == 'no_name' or screen == 'waiting':
                        if event.key == pg.K_RETURN:
                            if screen != 'waiting':
                                if len(self.g.curr_player) == 0:
                                    screen = 'no_name'
                                    print("INVALID NAME! Your name cannot be blank!")
                                else:
                                    if self.g.name_available or self.g.curr_player == old_name:
                                        screen = 'character'
                                        if not enteredName:
                                            # if not entered yet - connect once
                                            enteredName = True
                                            old_name = self.g.curr_player
                                            self.g.connectPlayer(self.g.curr_player)
                                        elif enteredName:
                                            # if entered once - just change name
                                            self.g.editPlayerName(old_name, self.g.curr_player)
                                            old_name = self.g.curr_player
                                    elif not self.g.name_available:
                                        print("NAME EXISTS! Enter a unique one!")
                            
                            else:
                                if player_ready and self.g.all_ready:
                                    self.g.startGame()

                        else:
                            # limit character length for the screen
                            if len(self.g.curr_player) < 10:
                                char = event.unicode
                                self.g.curr_player += char
            
            if screen == 'name' or screen == 'no_name':
                keys = pg.key.get_pressed()
                if keys[pg.K_BACKSPACE]:
                    self.g.curr_player = self.g.curr_player[:-1]

            if screen == 'character':
                self.g.screen.blit(mario.image, (mario.x, mario.y))
                self.g.screen.blit(luigi.image, (luigi.x, luigi.y))
                self.g.screen.blit(yoshi.image, (yoshi.x, yoshi.y))
                self.g.screen.blit(popo.image, (popo.x, popo.y))
                self.g.screen.blit(nana.image, (nana.x, nana.y))
                self.g.screen.blit(link.image, (link.x, link.y))

            elif screen == 'waiting':
                self.g.screen.blit(ready.image, (ready.x, ready.y))

            if not player_ready:
                self.g.screen.blit(back.image, (back.x, back.y))

            pg.display.flip()

    def drawStats(self):
        # see notes.txt in root folder
        mario = ['3', '6', '50']
        luigi = ['4', '8', '40']
        yoshi = ['5', '10', '30']
        popo = ['5.5', '11', '25']
        nana = ['5.7', '11', '22']
        link = ['6', '12', '20']        
        
        font = pg.font.Font(None, 30)

        for i in range(0, 6):
            if i == 0:
                x = 106
                char = mario
            elif i == 1:
                x = 295
                char = luigi
            elif i == 2:
                x = 470
                char = yoshi
            elif i == 3:
                x = 648
                char = popo
            elif i == 4:
                x = 824
                char = nana
            elif i == 5:
                x = 1001
                char = link
            for j in range(0,3):
                if j == 0:
                    y = 581
                elif j == 1:
                    y = 606
                elif j == 2:
                    y = 631
                text = font.render(char[j], True, WHITE)
                self.g.screen.blit(text, (x, y))
