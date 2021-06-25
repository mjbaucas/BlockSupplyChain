import time
import socket
import os
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((socket.gethostname(), 80))
server.listen(3)

try:
    while True:
        try:    
            connection, address = server.accept()
            packet = connection.recv(1024).decode()
            print(packet)
        except Exception as e:
            print(e)
except KeyboardInterrupt:
    server.shutdown(socket.SHUT_RDWR)
    connection.close()
    server.close()
    sys.exit()

