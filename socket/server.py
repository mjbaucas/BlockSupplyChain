import time
import socket
import os
import sys
import json
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
            packet = json.loads(packet)
            if priv_mngr.check_user(packet['user'], packet['password']):
                counter[packet['user']]+=1
                print(counter)
        except Exception as e:
            print(e)
except KeyboardInterrupt:
    print(priv_mngr.blockchain)
    print(str(counter))
    server.shutdown(socket.SHUT_RDWR)
    connection.close()
    server.close()
    sys.exit()

