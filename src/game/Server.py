'''

Here is the API for the server:

NOTE - This can be improved if something like json is used.

======================================================================

CONNECT <name>
- connects player to game

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

UPDATE_PLAYER
- repeatedly updates status, health, and position of one player

UPDATE_ALL_PLAYERS
- repeatedly updates status, health, and position of all players

======================================================================

Player values (space delimiter):
name: status character charHealth charXPos charYPos

======================================================================

Player statuses:
ready
unready
alive
dead

'''

from settings import *
import socket

# server parameters
HOST = 'localhost'
PORT = 10000
BUFFER = 1024
SERVER = (HOST, PORT)

# binding the socket to the port
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(SERVER)

players = {}
playersReady = 0
game = WAITING

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
        players[message[1]] = 'unready none 100 0 0'

    # remove player from players list
    elif action == 'DISCONNECT':
        print('{} has disconnected!'.format(message[1]))
        players.pop(message[1])

    # change if name of player passed is different
    elif action == 'EDIT_NAME':
        if message[1] != message[2]:
            print('{} has changed name to {}'.format(message[1], message[2]))
            players[message[2]] = players.pop(message[1])

    # change value of the character which is initially 'none'
    elif action == 'EDIT_CHARACTER':
        print('{} picked {}'.format(message[1], message[2]))
        playerValues = players[message[1]].split()
        playerValues[1] = message[2]
        playerValues = ' '.join(playerValues)
        players[message[1]] = playerValues

    # change value of the status (check API for more)
    elif action == 'EDIT_STATUS':
        print('{} is now {}'.format(message[1], message[2]))
        playerValues = players[message[1]].split()
        playerValues[0] = message[2]
        playerValues = ' '.join(playerValues)
        players[message[1]] = playerValues

        if message[2] == 'ready':
            playersReady += 1
        elif message[2] == 'unready':
            playersReady -= 1

    # return number of players ready
    elif action == 'PLAYERS_READY':
        data = 'PLAYERS_READY '
        data += str(playersReady)
        data = str.encode(data)

    elif action == 'START_GAME':
        if playersReady >= 1 and playersReady <= 6:
            data = 'START_GAME '
            i = 0
            for key, value in players.items():
                values = value.split(' ')
                # initialize the coordinates of all players
                # 0 - status | 1 - character (permanent) | 2 - health | 3 - xPos | 4 - yPos
                
                # these x and y values are hardcoded depending on the amount of players
                if i == 0:
                    values[3] = '157'
                    values[4] = '0'
                elif i == 1:
                    values[3] = '534'
                    values[4] = '0'
                elif i == 2:
                    values[3] = '345'
                    values[4] = '0'
                elif i == 3:
                    values[3] = '157'
                    values[4] = '600'
                elif i == 4:
                    values[3] = '534'
                    values[4] = '600'
                elif i == 5:
                    values[3] = '345'
                    values[4] = '400'

                i += 1
                values = ' '.join(values)
                data += key + ' ' + values + '|'

            data = str.encode(data)
            game = GAME
    
    elif action == 'JOIN_GAME':
        data = 'JOIN_GAME '
        data += str(game)
        data = str.encode(data)

    elif action == 'UPDATE_PLAYER':
        data = 'UPDATE_PLAYER '

        name = message[1]
        status = message[2]
        health = message[3]
        xPos = message[4]
        yPos = message[5]

        values = players[name].split()
        # 0 - status | 1 - character (permanent) | 2 - health | 3 - xPos | 4 - yPos
        values[0] = status
        values[2] = health
        values[3] = xPos
        values[4] = yPos
        players[name] = ' '.join(values)

        data += name + ' ' + status + ' ' + health + ' ' + xPos + ' ' + yPos
        data = str.encode(data)
    
    elif action == 'UPDATE_ALL_PLAYERS':
        data = 'UPDATE_ALL_PLAYERS '
        
        for key, value in players.items():
            data += key + ' ' + value + '|'

        data = str.encode(data)

    # send the response back to the client
    if data:
        s.sendto(data, address)
