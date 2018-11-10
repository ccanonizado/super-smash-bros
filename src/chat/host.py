import chat_pb2
import socket

HOST = '202.92.144.45'
PORT = 80

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    chat = chat_pb2.TcpPacket()
    chat.type = chat_pb2.TcpPacket.CREATE_LOBBY

    lobby = chat.CreateLobbyPacket()
    lobby.type = chat_pb2.TcpPacket.CREATE_LOBBY
    lobby.max_players = 3

    s.send(lobby.SerializeToString())

    data = s.recv(1024)

    lobby.ParseFromString(data)

    lobby_id = lobby.lobby_id

    print(lobby_id)