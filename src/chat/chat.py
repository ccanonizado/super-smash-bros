import chat_pb2
import socket
import select
from threading import Thread

thread = Thread()
packet = chat_pb2.TcpPacket()

# server parameters
HOST = '202.92.144.45'
PORT = 80
BUFFER = 1024

def printMenu():
	print("[1] Host")
	print("[2] Chat")
	print("[3] Exit")
	print("Choice: ", end="")

def createLobby(packet):
	packet.type = chat_pb2.TcpPacket.CREATE_LOBBY

	lobby = packet.CreateLobbyPacket()
	lobby.type = packet.type

	print("Enter max players: ", end="")
	lobby.max_players = int(input())
	return lobby

def listPlayers(packet):
	packet.type = chat_pb2.TcpPacket.PLAYER_LIST

	players = packet.PlayerListPacket()
	players.type = packet.type

	return players

def connectToLobby(packet):
	packet.type = chat_pb2.TcpPacket.CONNECT

	connect = packet.ConnectPacket()
	connect.type = packet.type

	print("Enter lobby id: ", end="")
	connect.lobby_id = input()

	print("Enter your name: ", end="")
	connect.player.name = input()

	return connect

def chatInLobby(packet, message):
	packet.type = chat_pb2.TcpPacket.CHAT

	chat = packet.ChatPacket()
	chat.type = packet.type

	chat.message = message

	return chat

def disconnectChat(packet):
	packet.type = chat_pb2.TcpPacket.DISCONNECT

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))

	while(True):
		printMenu()
		choice = int(input())

		# host
		if choice == 1:
			print()
			lobby = createLobby(packet)

			s.send(lobby.SerializeToString())
			data = s.recv(BUFFER)

			lobby.ParseFromString(data)
			lobby_id = lobby.lobby_id
			print("Created lobby: {}".format(lobby_id))
			print()

		# chat
		elif choice == 2:
			print()
			connect = connectToLobby(packet)

			s.send(connect.SerializeToString())
			data = s.recv(BUFFER)

			print()
			print("Welcome to Chat Lobby {}!".format(connect.lobby_id))
			print("Type lp() to list active players. Enjoy!")
			print()

			while(True):
				print("Enter message (q to quit): ", end="")
				message = input()

				if message == "lp()":
					players = listPlayers(packet)

					s.send(players.SerializeToString())
					data = s.recv(BUFFER)

					players.ParseFromString(data)
					print("Current players: ", end="")
					print(players.player_list)

				elif message == 'q':
					print("You have been disconnected.")
					print()
					break

				else:
					chat = chatInLobby(packet, message)

					s.send(chat.SerializeToString())
					data = s.recv(BUFFER)

					chat.ParseFromString(data)

					print("{}: {}".format(chat.player.name, chat.message))

		# exit
		elif choice == 3:
			break

		else:
			print("Invalid choice!")