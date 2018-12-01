import socket

# server parameters
HOST = 'localhost'
PORT = 10000
BUFFER = 1024

# binding the socket to the port
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

players = []

while True:
    data, address = s.recvfrom(4096)

    print(data.decode())

    if data:
        sent = s.sendto(data, address)
