'''

Here is the API for the server:

======================================================================

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

CREATE_CHAT
- creates a chat lobby given the number of players in the game

JOIN_CHAT
- joins existing lobby from CREATE_CHAT

UPDATE_PLAYER
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

# server parameters
HOST = '0.0.0.0'
PORT = 10000
BUFFER = 1024
SERVER = (HOST, PORT)

# binding the socket to the port
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(SERVER)

players = {}
init_players = {}
restart_count = 0
players_ready = 0
game = WAITING
chat_lobby = 0

print('Server is now up and running!')
print('There must be 3-6 players ready before starting the game.')
print('Just look here for updates whenever the client "Game.py" does something.')
print()
print('UPDATES:')

# once server receives something - check API - update - then return
while True:
    data, address = s.recvfrom(BUFFER)

    message = data.decode().split()
    action = message[0]

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

    # change value of the status (check API for more)
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

    elif action == 'START_GAME':
        if players_ready >= 1 and players_ready <= 6:
            data = 'START_GAME '
            i = 0

            for player in players.values():
                # these x and y values are hardcoded depending on the amount of players
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

            init_players = copy.deepcopy(players)
            data += json.dumps(players)
            data = str.encode(data)
            game = GAME

    elif action == 'RESTART_REQUEST':
        restart_count += 1

    elif action == 'RESTART_GAME':
        data = 'NONE'
        data = str.encode(data)
        if (restart_count % len(players)) == 0:
            players = copy.deepcopy(init_players)
            data = 'RESTART_GAME '
            data += json.dumps(init_players)
            data = str.encode(data)
            game = GAME
    
    elif action == 'JOIN_GAME':
        data = 'JOIN_GAME '
        data += str(game)
        data = str.encode(data)

    elif action == 'CREATE_CHAT':
        chat_lobby = message[1]
        print("Created chat lobby: {}".format(message[1]))
        print("Players joined the lobby!")

    elif action == 'JOIN_CHAT':
        data = 'JOIN_CHAT '
        data += str(chat_lobby)
        data = str.encode(data)

    elif action == 'UPDATE_PLAYER':
        message.pop(0)
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
    
    elif action == 'UPDATE_ALL_PLAYERS':
        data = 'UPDATE_ALL_PLAYERS '
        data += json.dumps(players)
        data = str.encode(data)

    elif action == 'ATTACK_PLAYER':
        health = float(players[message[1]]['health'])
        new_health = health - float(message[2])
        players[message[1]]['health'] = str(new_health)
        players[message[1]]['move'] = message[3]

        # health cannot be less than 0
        if float(players[message[1]]['health']) < 0:
            players[message[1]]['health'] = '0'

    elif action == 'QUIT_GAME':
        print('One player quit! Reset the server if you want to play again.')
        data = 'QUIT_GAME'
        game = QUIT
        data = str.encode(data)

    elif action == 'GET_STATUS':
        data = 'GET_STATUS '
        data += str(game)
        data = str.encode(data)

    # send the response back to the client
    if data:
        # to see which action is the problem - uncomment line below
        # print(action)
        s.sendto(data, address)
