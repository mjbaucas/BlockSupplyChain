import time
import socket
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), 80))
server.listen(5)

try:
    while True:
        try:    
            connection, address = server.accept()
            packet = connection.recv(1024).decode()
            print(packet)
        except Exception as e:
            print(e)
except KeyboardInterrupt:
    pass

server.shutdown(socket.SHUT_RDWR)
connection.close()
server.close()