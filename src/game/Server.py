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

JOIN_GAME
- repeatedly attempts to join game if it has started

CREATE_CHAT <lobby_id>
- creates a chat lobby given the number of players in the game

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

GET_STATUS
- returns current status of the game

CHECK_WINNER
- for end game detection

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
PORT = 10000
BUFFER = 1024
SERVER = (HOST, PORT)

# binding the socket to the port
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(SERVER)

players = {} # players dict with attributes
init_players = {} # copy of initial players (for restarting)
players_ready = 0 # must be equal to len(players) to start
restart_count = 0 # must be equal to len(players) to restart
chat_lobby = '' # lobby_id to be broadcasted to everyone
game_status = WAITING # check settings.py for all game statuses

print('Server is now up and running!')
print('There must be 3-6 players ready before starting the game.')
print('Just look here for updates whenever the client "Game.py" does something.')
print()
print('UPDATES:')

# once server receives something - check API - update - then return
while True:
    data, address = s.recvfrom(BUFFER)

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
            'move': 'stand'
        }

    # remove player from players list
    elif action == 'DISCONNECT':
        print('{} has disconnected!'.format(message[1]))
        players.pop(message[1])

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
        print('{} is now {}'.format(message[1], message[2]))
        players[message[1]]['status'] = message[2]

        if message[2] == 'ready':
            players_ready += 1
        elif message[2] == 'unready':
            players_ready -= 1

    # return number of players ready
    elif action == 'PLAYERS_READY':
        data = 'PLAYERS_READY '
        data += str(players_ready)
        data = str.encode(data)

    # check line 184 for the condition for the game to start
    elif action == 'START_GAME':
        if players_ready == len(players) and len(players) >= 1:
            data = 'START_GAME '
            
            i = 0
            for player in players.values():
                # these x and y values are hardcoded depending on the amount of players
                # for positioning them correctly in the game arena
                if i == 0:
                    player['xPos'] = '157'
                    player['yPos'] = '0'
                    player['direc'] = 'right'
                elif i == 1:
                    player['xPos'] = '534'
                    player['yPos'] = '0'
                    player['direc'] = 'left'
                elif i == 2:
                    player['xPos'] = '345'
                    player['yPos'] = '0'
                    player['direc'] = 'right'
                elif i == 3:
                    player['xPos'] = '157'
                    player['yPos'] = '600'
                    player['direc'] = 'right'
                elif i == 4:
                    player['xPos'] = '534'
                    player['yPos'] = '600'
                    player['direc'] = 'left'
                elif i == 5:
                    player['xPos'] = '345'
                    player['yPos'] = '400'
                    player['direc'] = 'left'
                i += 1

            # create a copy of initial players if ever they want to request
            init_players = copy.deepcopy(players)

            data += json.dumps(players)
            data = str.encode(data)
            game_status = GAME

    # increment restart_count
    elif action == 'RESTART_REQUEST':
        restart_count += 1

    # repeatedly send at the end of the game
    elif action == 'RESTART_GAME':
        # action must be NONE if condition is not satisfied (line 233)
        data = 'NONE'
        data = str.encode(data)
        if (restart_count % len(players)) == 0:

            # replace current players with the initial ones
            players = copy.deepcopy(init_players)

            data = 'RESTART_GAME '
            data += json.dumps(init_players)
            data = str.encode(data)
            game_status = GAME
    
    # simply returns game status - client will evaluate
    elif action == 'JOIN_GAME':
        data = 'JOIN_GAME '
        data += str(game_status)
        data = str.encode(data)

    # chat lobby is created in client and passed here
    elif action == 'CREATE_CHAT':
        chat_lobby = message[1]
        print("Created chat lobby: {}".format(message[1]))
        print("Players joined the lobby!")
        print("Game is now running.")

    # if lobby is created - server broadcasts lobby_id
    elif action == 'JOIN_CHAT':
        data = 'JOIN_CHAT '
        data += str(chat_lobby)
        data = str.encode(data)

    # update single player
    elif action == 'UPDATE_PLAYER':
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

        players[name]['status'] = status
        players[name]['xPos'] = xPos
        players[name]['yPos'] = yPos
        players[name]['direc'] = direc
        players[name]['walk_c'] = walk_c
        players[name]['move'] = move
    
    # broadcast all player updates
    elif action == 'UPDATE_ALL_PLAYERS':
        data = 'UPDATE_ALL_PLAYERS '
        data += json.dumps(players)
        data = str.encode(data)

    # similar to update player but for decreasing the health
    elif action == 'ATTACK_PLAYER':
        health = float(players[message[1]]['health'])
        new_health = health - float(message[2])
        players[message[1]]['health'] = str(new_health)
        players[message[1]]['move'] = message[3]

        # health cannot be less than 0
        if float(players[message[1]]['health']) < 0:
            players[message[1]]['health'] = '0'

    # changes game status to QUIT
    elif action == 'QUIT_GAME':
        print('One player quit! Resetting server data.')
        print()
        print("NEW UPDATES:")
        data = 'QUIT_GAME'
        data = str.encode(data)
        game_status = WAITING

        # reset server data
        players = {}
        init_players = {}
        players_ready = 0
        restart_count = 0
        chat_lobby = ''

    # consistently returns the game status
    elif action == 'GET_STATUS':
        data = 'GET_STATUS '
        data += str(game_status)
        data = str.encode(data)

    #end game detection
    elif action == 'CHECK_WINNER':
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
    if data:
        # to see which action is the problem - uncomment line below
        # print(action)
        s.sendto(data, address)
