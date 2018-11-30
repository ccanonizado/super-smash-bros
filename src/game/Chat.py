import os
import sys

# for adding the path to the folder with the protobuf files
script_dir = sys.path[0]
script_dir = script_dir[:-4]
chat_path = os.path.join(script_dir, 'proto/')
sys.path.insert(0, chat_path)

from threading import Thread
import tcp_packet_pb2
import socket
import select

packet = tcp_packet_pb2.TcpPacket()
chatted = False

# server parameters
HOST = '202.92.144.45'
PORT = 80
BUFFER = 1024

class Chat:
	def __init__(self, game):
		self.game = game
		self.packet = packet
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((HOST,PORT))

		# connect socket to server
		# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		# 	self.s = s.connect((HOST, PORT))
			# while(True and not chatted):
			# 	chatted = True
			# 	print()
			# 	connect = connectToLobby(packet)
			# 	connect = sendAndReceive(connect, s)
			# 	print()
			# 	print("Welcome to Chat Lobby {}!".format(connect.lobby_id))
			# 	print("Type lp() to list active players. Enjoy!")
			# 	print()

			# 	sys.stdout.write("Enter message (q to quit): \n")
			# 	sys.stdout.flush()
			# 	while(True):
			# 		r, w, x = select.select([sys.stdin, s], [], [])
			# 		if not r:
			# 			continue
			# 		if r[0] is sys.stdin:
			# 			message = input()
			# 			if message == "q":
			# 				disconnect = disconnectChat(packet)
			# 				s.send(disconnect.SerializeToString())
			# 				print("You have been disconnected!")
			# 				s.close()
			# 				break
			# 			elif message == "lp()":
			# 				players = listPlayers(packet)
			# 				players = sendAndReceive(players, s)
			# 				print("Current players: ", end="")
			# 				for player in players.player_list:
			# 					print("{} ".format(player.name), end="")
			# 				print()
			# 			else:
			# 				chat = chatInLobby(packet, message)
			# 				s.send(chat.SerializeToString())
			# 				sys.stdout.flush()
					# else:
					# 	chat = packet.ChatPacket()
					# 	data = s.recv(BUFFER)
					# 	packet.ParseFromString(data)
					# 	if(packet.type == packet.CHAT):
					# 		chat.ParseFromString(data)
					# 		print("{}: {}".format(chat.player.name, chat.message))
					# 	elif(packet.type == packet.DISCONNECT):
					# 		disconnect = packet.DisconnectPacket()
					# 		disconnect.ParseFromString(data)
					# 		print("{} has disconnected!".format(disconnect.player.name))


	def startChat(self):
		while(True):
			chat = self.packet.ChatPacket()
			data = self.s.recv(BUFFER)
			self.packet.ParseFromString(data)
			if(self.packet.type == self.packet.CHAT):
				chat.ParseFromString(data)
				self.game.chat_messages.append('{}: {}'.format(chat.player.name, chat.message))
				# print("{}: {}".format(chat.player.name, chat.message))
			elif(self.packet.type == self.packet.DISCONNECT):
				disconnect = self.packet.DisconnectPacket()
				disconnect.ParseFromString(data)
				self.game.chat_messages.append('{} has disconnected!'.format(disconnect.player.name))
				print("{} has disconnected!".format(disconnect.player.name))

	# for moularization
	def sendAndReceive(self, packet):
		self.s.send(packet.SerializeToString())
		data = self.s.recv(BUFFER)
		packet.ParseFromString(data)
		return packet

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

		Thread(target=self.startChat).start()

	def listPlayers(self):
		players = self.packet.PlayerListPacket()
		players.type = self.packet.PLAYER_LIST

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

		return disconnect

