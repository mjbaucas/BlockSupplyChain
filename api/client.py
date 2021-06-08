import requests
import json
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

url = 'http://192.168.2.221:3000/send_rfid'
data = {}

device_id = "test_rfid_device_01"
password = "password1234"

try:
    while True:
        try:
            id, text = reader.read()
            print(id)
            print(text)
            timestamp = int(round(time.time() * 1000))
            packet = {"credentials":{"userid": device_id, "password": password}, "data": [id, timestamp]}
            temp_value = requests.post(url, json=json.dumps(packet), headers={'Content-Type': 'application/json', 'X-Api-Key' : ''})
        except Exception:
            pass
except KeyboardInterrupt:
    pass 

GPIO.cleanup()

