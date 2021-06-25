import sys
import time
import socket
import os

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    while True:
        try:
            tag, text = reader.read()
            route = sys.argv[1]
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((route, 80))
            print(tag)
            client.send(str.encode(str(tag)))
        except Exception as e:
            print(e)
except KeyboardInterrupt:
    pass

client.shutdown(socket.SHUT_RDWR)
client.close()
GPIO.cleanup()

