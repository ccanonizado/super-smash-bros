# not actual the client code - just for testing and code to be reused

import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
message = 'hello'

try:
    sent = s.sendto(str.encode(message), server_address)
    data, server = s.recvfrom(4096)
    print(data.decode())

finally:
    s.close()

'''
if choice == 'create':
    # count validation
    if error == 'none-success':
        self.status = GAME
        break
    elif text == '' or int(text) < 3 or int(text) > 6:
        error = 'invalid'
    else:
        # after lobby is created it connects to it
        print('Trying to connect to lobby - please wait!')
        error = 'none-success'
        self.chat = Chat(self)
        lobby = self.chat.createLobby(int(text))
        text = lobby.lobby_id
        self.lobby = lobby.lobby_id
        print('Lobby created: {}'.format(self.lobby))
        self.chat.connectToLobby(self.lobby, 'Cholo')
'''