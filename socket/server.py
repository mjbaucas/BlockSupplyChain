import time
import socket
import os

try:
    while True:
        try: 
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(("", 32500))
            server.listen(5)
            connection, address = server.accept()
            packet = connection.recv(1024)
            server.shutdown(socket.SHUT_RDWR)
            server.close()
            bound = True		
        except Exception as e:
            print(e)
except KeyboardInterrupt:
    pass

connection.close()
server.close()