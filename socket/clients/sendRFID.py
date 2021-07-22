import sys
import time
import socket
import os
import json

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

device_id = "test_rfid_device_01"
password = "password1234"

global_start = time.time()
time_limit = 600000

total = 0
counter = 0

try:
    while True:
        try:
            tag, text = reader.read()
            route = sys.argv[1]
            start = time.time()
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((route, 5000))
            temp_dict = {'user': device_id, 'password': password, 'data': tag}
            client.send(str.encode(json.dumps(temp_dict)))
            elapsed = (time.time()-start)*1000
            total+= elapsed
            counter+=1
            print('time taken: ' + str(elapsed) + ' ms')
            if time.time() > global_start + time_limit:
                break
        except Exception as e:
            print(e)
        time.sleep(2)
except KeyboardInterrupt:
    print('average:' + str(float(total/counter)))
    pass

client.shutdown(socket.SHUT_RDWR)
client.close()
GPIO.cleanup()

