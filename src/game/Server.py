'''

Here is the API for the server:

======================================================================

NOTE - first string is always the action (next fields are optional)

CONNECT <name>
- connects player to game

CHECK_NAME <name>
- checks if name is taken returns 'taken' or 'free'

EDIT_NAME <old_name> <new_name>
- edits player's name if connected

EDIT_CHARACTER <name> <character>
- edits player's character

EDIT_STATUS <name>
- edits player's status (check statuses below)

DISCONNECT <name>
- disconnects player

PLAYERS_READY <num_of_players>
- returns number of players ready

START_GAME
- if number of players is sufficient then game starts
- all players' x and y positions are updated to fit the game screen

JOIN_CHAT
- joins existing lobby from CREATE_CHAT

UPDATE_PLAYER <player>
- repeatedly updates status, health, and position of one player

UPDATE_ALL_PLAYERS
- repeatedly updates status, health, and position of all players

ATTACK_PLAYER <player> <damage>
- player is being attacked with N damage

RESTART_REQUEST
- one player wants to restart the game

RESTART_GAME
- if everyone wants to restart the game - it will be reset

QUIT_GAME
- if one player presses Esc - everyone disconnects

CHECK_WINNER
- for end game detection

CHECK_READY
- checks if everyone is ready

CHECK_DISCONNECT
- checks if there is someone who recently disconnected

======================================================================

NOTE - for reference
name: {
    name: - <string>
    status: ready / unready / alive / dead | <string>
    character: - <string>
    health: - <int>
    xPos: - <float>
    yPos: - <float>
    direc: - (direction) | <string>
    walk_c: - (walk count) | <int>
    move: - walk / stand / attack / damaged / dead | <string>
}

======================================================================

Player statuses:
ready
unready
alive
dead

'''

from Chat import Chat
from settings import *
import socket
import json
import copy
import sys

if len(sys.argv) == 1:
    HOST = '0.0.0.0'
else:
    HOST = sys.argv[1]

# server parameters
PORT = 8000
BUFFER = 2048
SERVER = (HOST, PORT)

# binding the socket to the port
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(SERVER)

sessions = 1 # number of times the game has been reset
players = {} # players dict with attributes
init_players = {} # copy of initial players (for restarting)
players_ready = 0 # must be equal to len(players) to start
restart_count = 0 # must be equal to len(players) to restart
chat_lobby = '' # lobby_id to be broadcasted to everyone
game_started = False # checks if existing game has started
game_status = WAITING # check settings.py for all game statuses
recent_disconnect = '' # name of player who recently disconnected

print('Server is now up and running!')
print('There must be 2-6 players ready before starting the game.')
print('Just look here for updates whenever the client "Game.py" does something.')
print()
print('SESSION #{} UPDATES:'.format(sessions))

message_count = 0

# once server receives something - check API - update - then return
while True:
    data, address = s.recvfrom(BUFFER)

    if data:
        message = data.decode().split()
        action = message[0] # first message is the action

        # add player to player list and add initial character values
        if action == 'CONNECT':
            print('{} has connected!'.format(message[1]))
            players[message[1]] = {
                'character': 'none',
                'status': 'unready',
                'health': '100',
                'xPos': '0',
                'yPos': '0',
                'direc': 'right',
                'walk_c': '0',
                'move': 'stand',
                'address': address
            }

        # remove player from players list and return player name
        elif action == 'DISCONNECT':
            print('{} has disconnected!'.format(message[1]))
            players.pop(message[1])
            players_ready -= 1
            if(players_ready) < 0:
                players_ready = 0
            
            if message[2] == 'TRUE':
                restart_count -= 1

            recent_disconnect = message[1]

            # remove player from initial list - for the restart
            if message[1] in init_players:
                init_players.pop(message[1])

            data = 'DISCONNECT '
            data += message[1]
            data = str.encode(data)

            # if there are no more players - reset 
            if len(players) == 0 and game_status == GAME:
                
                # increment sessions
                sessions += 1

                print('Resetting server data for new session.')
                print()
                print('SESSION #{} UPDATES:'.format(sessions))
                
                # reset server data
                players = {}
                init_players = {}
                players_ready = 0
                restart_count = 0
                chat_lobby = ''
                game_started = False
                game_status = WAITING
                recent_disconnect = ''

            # if this player disconnected - check if eligible for restart
            elif game_status != WAITING and (restart_count % len(players)) == 0:
                # replace current players with the initial ones
                players = copy.deepcopy(init_players)

                print("===== Restarted Game! =====")

                data = 'RESTART_GAME '
                data += json.dumps(init_players)
                data = str.encode(data)
                game_status = GAME

                for player in players.values():
                    s.sendto(data, player['address'])

        # returns name of player who recently disconnected
        elif action == 'CHECK_DISCONNECT':
            data = 'CHECK_DISCONNECT '
            data += recent_disconnect
            data = str.encode(data)

        # checks if name is in the players dict
        elif action == 'CHECK_NAME':
            data = 'CHECK_NAME '
            if len(message) == 1:
                data += 'free'
            else:
                if message[1] in players:
                    data += 'taken'
                else:
                    data += 'free'
            data = str.encode(data)

        # change if name of player passed is different
        elif action == 'EDIT_NAME':
            if message[1] != message[2]:
                print('{} has changed name to {}'.format(message[1], message[2]))
                players[message[2]] = players.pop(message[1])

        # change value of the character which is initially 'none'
        elif action == 'EDIT_CHARACTER':
            print('{} picked {}'.format(message[1], message[2]))
            players[message[1]]['character'] = message[2]

        # change value of the player's status (check API for more)
        elif action == 'EDIT_STATUS':
            players[message[1]]['status'] = message[2]

            players_ready = 0
            for player in players.values():
                if player['status'] == 'ready':
                    players_ready += 1

        # starts game and sends to all player addresses
        elif action == 'START_GAME':
            data = 'NONE'
            if players_ready == len(players) and len(players) >= 2 and len(players) <= 6:
                if not game_started:
                    print("====== Started Game! ======")
                    game_started = True
                    game_status = GAME

                    # try:
                    #     chat = Chat()
                    #     chat_lobby = chat.createLobby(6).lobby_id
                    #     print("Created chat lobby: {}".format(chat_lobby))

                    #     # broadcast chat_lobby to everyone
                    #     data = 'JOIN_CHAT '
                    #     data += str(chat_lobby)
                    #     data = str.encode(data)

                    #     for player in players.values():
                    #         s.sendto(data, player['address'])

                    # except:
                    #     print("CHAT ERROR! Server might be down.")

                    i = 0
                    for player in players.values():
                        # these x and y values are hardcoded depending on the amount of players
                        # for positioning them correctly in the game arena
                        if i == 0:
                            player['xPos'] = '157'
                            player['yPos'] = '480'
                            player['direc'] = 'right'
                        elif i == 1:
                            player['xPos'] = '534'
                            player['yPos'] = '480'
                            player['direc'] = 'left'
                        elif i == 2:
                            player['xPos'] = '345'
                            player['yPos'] = '260'
                            player['direc'] = 'right'
                        elif i == 3:
                            player['xPos'] = '157'
                            player['yPos'] = '680'
                            player['direc'] = 'right'
                        elif i == 4:
                            player['xPos'] = '534'
                            player['yPos'] = '680'
                            player['direc'] = 'left'
                        elif i == 5:
                            player['xPos'] = '345'
                            player['yPos'] = '680'
                            player['direc'] = 'left'
                        i += 1

                    # create a copy of initial players if ever they want to request restart
                    init_players = copy.deepcopy(players)

                    data = 'START_GAME '
                    data += json.dumps(players)
                    data = str.encode(data)
                    game_status = GAME

                    for player in players.values():
                        s.sendto(data, player['address'])

        # changes game status to QUIT
        elif action == 'QUIT_GAME':
            
            # increment sessions
            sessions += 1

            print('Resetting server data for new session.')
            print()
            print('SESSION #{} UPDATES:'.format(sessions))
            data = 'QUIT_GAME'
            data = str.encode(data)
            
            for player in players.values():
                s.sendto(data, player['address'])

            data = 'NONE'

            # reset server data
            players = {}
            init_players = {}
            players_ready = 0
            restart_count = 0
            chat_lobby = ''
            game_started = False
            game_status = WAITING
            recent_disconnect = ''

        # increment restart_count
        elif action == 'RESTART_REQUEST' and game_status != WAITING:
            restart_count += 1

            if (restart_count % len(players)) == 0:
                # replace current players with the initial ones
                players = copy.deepcopy(init_players)

                print("===== Restarted Game! =====")

                data = 'RESTART_GAME '
                data += json.dumps(init_players)
                data = str.encode(data)
                game_status = GAME

                for player in players.values():
                    s.sendto(data, player['address'])

                continue

        # update single player
        elif action == 'UPDATE_PLAYER' and game_status != WAITING:
            message.pop(0) # remove action
            message = ' '.join(message)
            payload = json.loads(message)

            name = payload['name']
            status = payload['status']
            xPos = payload['xPos']
            yPos = payload['yPos']
            direc = payload['direc']
            walk_c = payload['walk_c']
            move = payload['move']

            if float(yPos) > 700:
                yPos = '30'

            players[name]['status'] = status
            players[name]['xPos'] = xPos
            players[name]['yPos'] = yPos
            players[name]['direc'] = direc
            players[name]['walk_c'] = walk_c
            players[name]['move'] = move

        # updates all players
        elif action == 'UPDATE_ALL_PLAYERS' and game_status != WAITING:
            data = 'UPDATE_ALL_PLAYERS '
            data += json.dumps(players)
            data = str.encode(data)

        # similar to update player but for decreasing the health
        elif action == 'ATTACK_PLAYER' and game_status != WAITING:
            health = float(players[message[1]]['health'])
            new_health = health - float(message[2])
            players[message[1]]['health'] = str(new_health)
            players[message[1]]['move'] = message[3]

            # health cannot be less than 0
            if float(players[message[1]]['health']) < 0:
                players[message[1]]['health'] = '0'
            
            data = 'UPDATE_ALL_PLAYERS '
            data += json.dumps(players)
            data = str.encode(data)

            for player in players.values():
                s.sendto(data, player['address'])

        #end game detection
        elif action == 'CHECK_WINNER' and game_status != WAITING:
            alive_count = len(players)
            alive = ''
            for key, value in players.items():
                if float(value['health']) == 0:
                    alive_count -= 1
                else:
                    alive = key

            # if there is a winner - return the player's name
            if alive_count <= 1:
                data = 'CHECK_WINNER '
                data += alive
                data = str.encode(data)
            else:
                data = 'NONE'
                data = str.encode(data)

        # send the response back to the client
        # NOTE - to see which action is the problem - uncomment line below
        # print(action)

        if data != 'NONE':
            s.sendto(data, address)

    # consistently sending if game state is waiting
    if game_status == WAITING and data != 'NONE':
        data = 'PLAYERS_READY '
        data += str(players_ready)
        data = str.encode(data)
        
        for player in players.values():
            s.sendto(data, player['address'])