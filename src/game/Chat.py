import os
import sys

# add the path to the folder with the protobuf files
script_dir = sys.path[0]
script_dir = script_dir[:-4]
chat_path = os.path.join(script_dir, 'proto/')
sys.path.insert(0, chat_path)

from threading import Thread
import tcp_packet_pb2
import socket
import select

# create main TcpPacket
packet = tcp_packet_pb2.TcpPacket()

# server parameters
HOST = '202.92.144.45'
PORT = 80
BUFFER = 1024

class Chat:
	def __init__(self, game):
		self.g = game
		self.packet = packet
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# connect to server
		self.s.connect((HOST,PORT))

	# to be executed in a thread after connectToLobby
	def receiveMessages(self):
		while(True):
			chat = self.packet.ChatPacket()
			data = self.s.recv(BUFFER)
			self.packet.ParseFromString(data)

			# there is a threshold of 20 messages for the GUI
			if(self.packet.type == self.packet.CHAT):
				chat.ParseFromString(data)
				if(len(self.g.chat_messages) == 20):
					self.g.chat_messages.pop(0)
				self.g.chat_messages.append('{}: {}'.format(chat.player.name, chat.message))
			
			# self.g.chat_messages -> list from Game.py
			elif(self.packet.type == self.packet.DISCONNECT):
				disconnect = self.packet.DisconnectPacket()
				disconnect.ParseFromString(data)
				if(len(self.g.chat_messages) == 20):
					self.g.chat_messages.pop(0)
				self.g.chat_messages.append('{} has disconnected!'.format(disconnect.player.name))

	# for moularization
	def sendAndReceive(self, packet):
		self.s.send(packet.SerializeToString())
		data = self.s.recv(BUFFER)
		packet.ParseFromString(data)
		return packet


	'''

	Format of methods from here:
	<instantation of packet and adding type>
	<SPACE>
	<adding of parameters>
	<SPACE>
	<sending and returning of packet if ever>

	'''

	def createLobby(self, number):
		lobby = self.packet.CreateLobbyPacket()
		lobby.type = self.packet.CREATE_LOBBY

		lobby.max_players = number

		lobby = self.sendAndReceive(lobby)
		return lobby

	def connectToLobby(self, lobby_id, name):
		connect = self.packet.ConnectPacket()
		connect.type = self.packet.CONNECT

		connect.lobby_id = lobby_id
		connect.player.name = name

		connect = self.sendAndReceive(connect)

		# run the thread for getting chat messages
		Thread(target=self.receiveMessages).start()

	def listPlayers(self):
		players = self.packet.PlayerListPacket()
		players.type = self.packet.PLAYER_LIST

		# no parameters

		players = self.sendAndReceive(players)
		return players

	def chatInLobby(self, message):
		chat = self.packet.ChatPacket()
		chat.type = self.packet.CHAT

		chat.message = message

		self.s.send(chat.SerializeToString())

	def disconnectChat(self):
		disconnect = self.packet.DisconnectPacket()
		disconnect.type = self.packet.type.DISCONNECT

		# no parameters

		self.sendAndReceive(disconnect)

