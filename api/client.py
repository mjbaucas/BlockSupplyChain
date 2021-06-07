import requests
import json
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

url = 'http://10.11.252.136:3000/send_rfid'
data = {}

counter = 0
for i in range(0,2):
    try:
        counter+=1
        id, text = reader.read()
        print(id)
        print(text)
        timestamp = int(round(time.time() * 1000))
        data[counter] = id
        temp_value = requests.post(url, json=json.dumps(data), headers={'Content-Type': 'application/json', 'X-Api-Key' : ''})
    finally:
        GPIO.cleanup()

