import time
import socket
import os
import sys
from managers import PrivateBlockchainManager

counter = {"test_rfid_device_01": 0, "test_temphumid_device_01": 0, "test_accel_device_01": 0, "test_motion_device_01": 0}

priv_mngr = PrivateBlockchainManager()

try:
    while True:
        try:    
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(("", 5000))
            server.listen(3)
            connection, address = server.accept()
            packet = connection.recv(2048).decode()
            if priv_mngr.check_user(packet['user'], packet['password']):
                counter['user']+=1
            print(packet)
        except Exception as e:
            print(e)
except KeyboardInterrupt:
    server.shutdown(socket.SHUT_RDWR)
    connection.close()
    server.close()
    print(str(counter))
    sys.exit()

