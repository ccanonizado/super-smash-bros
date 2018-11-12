import player_pb2
import tcp_packet_pb2
import socket
import select
import sys
from threading import Thread

thread = Thread()
packet = tcp_packet_pb2.TcpPacket()

# server parameters
HOST = '202.92.144.45'
PORT = 80
BUFFER = 1024

def sendAndReceive(packet, s):
	s.send(packet.SerializeToString())
	data = s.recv(BUFFER)
	packet.ParseFromString(data)
	return packet

def printMenu():
	print("[1] Host")
	print("[2] Chat")
	print("[3] Exit")
	print("Choice: ", end="")

def createLobby(packet):
	packet.type = packet.CREATE_LOBBY

	lobby = packet.CreateLobbyPacket()
	lobby.type = packet.type

	print("Enter max players: ", end="")
	lobby.max_players = int(input())
	return lobby

def listPlayers(packet):
	packet.type = packet.PLAYER_LIST

	players = packet.PlayerListPacket()
	players.type = packet.type

	return players

def connectToLobby(packet):
	packet.type = packet.CONNECT

	connect = packet.ConnectPacket()
	connect.type = packet.type

	print("Enter lobby id: ", end="")
	connect.lobby_id = input()

	print("Enter your name: ", end="")
	connect.player.name = input()

	return connect

def chatInLobby(packet, message):
	packet.type = packet.CHAT

	chat = packet.ChatPacket()
	chat.type = packet.type

	chat.message = message

	return chat

def disconnectChat(packet):
	packet.type = packet.DISCONNECT

	disconnect = packet.DisconnectPacket()
	disconnect.type = packet.type

	return disconnect

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))

	while(True):
		printMenu()
		choice = int(input())

		# host
		if choice == 1:
			print()
			lobby = createLobby(packet)
			lobby = sendAndReceive(lobby, s)
			lobby_id = lobby.lobby_id
			print("Created lobby: {}".format(lobby_id))
			print()

		# chat
		elif choice == 2:
			print()
			connect = connectToLobby(packet)
			connect = sendAndReceive(connect, s)
			print()
			print("Welcome to Chat Lobby {}!".format(connect.lobby_id))
			print("Type lp() to list active players. Enjoy!")
			print()

			sys.stdout.write("Enter message (q to quit): ")
			sys.stdout.flush()
			while(True):
				r, w, x = select.select([sys.stdin, s], [], [])
				if not r:
					continue
				if r[0] is sys.stdin:
					message = input()
					if message == "q":
						s.close()
						break
					elif message == "lp()":
						players = listPlayers(packet)
						players = sendAndReceive(players, s)
						print("Current players: ", end="")
						for player in players.player_list:
							print("{} ".format(player.name), end="")
						print()
					else:
						chat = chatInLobby(packet, message)
						s.send(chat.SerializeToString())
						sys.stdout.flush()
				else:
					chat = packet.ChatPacket()
					data = s.recv(BUFFER)
					chat.ParseFromString(data)
					print("{}: {}".format(chat.player.name, chat.message))

				# print("Enter message (q to quit): ", end="")
				# message = input()

				'''
				if message == "lp()":
					players = listPlayers(packet)
					players = sendAndReceive(players, s)
					print("Current players: ", end="")
					for player in players.player_list:
						print("{} ".format(player.name), end="")
					print()

				elif message == 'q':
					disconnect = disconnectChat(packet)
					disconnect = sendAndReceive(disconnect, s)
					print("You have been disconnected.")
					print()
					break

				else:
					chat = chatInLobby(packet, message)
					chat = sendAndReceive(chat, s)
					print("{}: {}".format(chat.player.name, chat.message))
				'''

		# exit
		elif choice == 3:
			break

		else:
			print("Invalid choice!")