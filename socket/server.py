import time
from datetime import datetime
import socket
import os
import sys
import inspect
import json
import mongoengine

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from api.database.models import RfidData, PrivateBlockData
from api.database.managers import PrivateBlockchainManager

counter = {"test_rfid_device_01": 0, "test_temphumid_device_01": 0, "test_accel_device_01": 0, "test_motion_device_01": 0}

mongoengine.connect(host='mongodb://localhost:27017/test')
priv_mngr = PrivateBlockchainManager(PrivateBlockData)

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
                if packet['type'] == 'rfid':
                    data = RfidData()
                    data.device = packet["user"]
                    data.tag = str(packet["data"])
                    data.timestamp = datetime.fromtimestamp(packet["timestamp"])
                    data.save()
                counter[packet['user']]+=1
                print(counter)
        except Exception as e:
            print(e)
except KeyboardInterrupt:
    print(str(counter))
    server.shutdown(socket.SHUT_RDWR)
    connection.close()
    server.close()
    sys.exit()

