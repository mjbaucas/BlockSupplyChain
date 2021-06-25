import sys
import time
import socket
import os

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

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
            client.send(str.encode(str(tag)))
            elapsed = (time.time()-start)*1000
            total+= elapsed
            counter+=1
            print('time taken: ' + str(elapsed) + ' ms')
        except Exception as e:
            print(e)
        time.sleep(2)
except KeyboardInterrupt:
    print('average:' + str(float(total/counter)))
    pass

client.shutdown(socket.SHUT_RDWR)
client.close()
GPIO.cleanup()

