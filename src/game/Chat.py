import os
import sys

# for adding the path to the folder with the protobuf files
script_dir = sys.path[0]
script_dir = script_dir[:-4]
chat_path = os.path.join(script_dir, 'proto/')
sys.path.insert(0, chat_path)

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
	def __init__(self):
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
			# 		else:
			# 			chat = packet.ChatPacket()
			# 			data = s.recv(BUFFER)
			# 			packet.ParseFromString(data)
			# 			if(packet.type == packet.CHAT):
			# 				chat.ParseFromString(data)
			# 				print("{}: {}".format(chat.player.name, chat.message))
			# 			elif(packet.type == packet.DISCONNECT):
			# 				disconnect = packet.DisconnectPacket()
			# 				disconnect.ParseFromString(data)
			# 				print("{} has disconnected!".format(disconnect.player.name))


	# for moularization
	def sendAndReceive(self, packet):
		self.s.send(packet.SerializeToString())
		data = self.s.recv(BUFFER)
		packet.ParseFromString(data)
		return packet

	def createLobby(self, packet, number):
		packet.type = packet.CREATE_LOBBY

		lobby = packet.CreateLobbyPacket()
		lobby.type = packet.type
		lobby.max_players = number

		lobby = self.sendAndReceive(lobby)
		return lobby

	def listPlayers(self, packet):
		packet.type = packet.PLAYER_LIST

		players = packet.PlayerListPacket()
		players.type = packet.type

		players = self.sendAndReceive(players)
		return players

	def connectToLobby(self, packet):
		packet.type = packet.CONNECT

		connect = packet.ConnectPacket()
		connect.type = packet.type

		print("Enter lobby id: ", end="")
		connect.lobby_id = input()

		print("Enter your name: ", end="")
		connect.player.name = input()

		return connect

	def chatInLobby(self, packet, message):
		packet.type = packet.CHAT

		chat = packet.ChatPacket()
		chat.type = packet.type

		chat.message = message

		return chat

	def disconnectChat(self, packet):
		packet.type = packet.DISCONNECT

		disconnect = packet.DisconnectPacket()
		disconnect.type = packet.type

		return disconnect

