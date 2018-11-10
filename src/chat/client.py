import chat_pb2
import socket

HOST = '202.92.144.45'
PORT = 80

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    chat = chat_pb2.TcpPacket()
    chat.type = chat_pb2.TcpPacket.CONNECT

    connect = chat.ConnectPacket()
    connect.type = chat_pb2.TcpPacket.CONNECT
    
    print("Enter lobby id: ", end="")
    connect.lobby_id = input()

    print("Enter your name: ", end="")    
    connect.player.name = input()

    s.send(connect.SerializeToString())

    while(True):
        chat.type = chat_pb2.TcpPacket.CHAT 
        
        message = chat.ChatPacket()
        message.type = chat_pb2.TcpPacket.CHAT

        print("Enter message: ", end="")
        message.message = input()

        s.send(message.SerializeToString())

        data = s.recv(1024)

        message = message.ParseFromString(data)

        print(data)