import requests
import json
from datetime import datetime
import time
import sys
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

device_id = "test_rfid_device_01"
password = "password1234"

url = 'http://' + sys.argv[1] + ':3000/send/rfid'

try:
    while True:
        try:
            tag, text = reader.read()
            #print(id)
            #print(text)
            timestamp = datetime.now().timestamp()
            packet = {"credentials":{"userid": device_id, "password": password}, "data": {"tag": tag, "timestamp": timestamp}}
            start = time.time()
            temp_value = requests.post(url, json=json.dumps(packet), headers={'Content-Type': 'application/json', 'X-Api-Key' : ''})
            print 'time taken ', (time.time()-start)*1000 ,' ms'
        except Exception as e:
            #print(e) # Uncomment for debugging  
            pass
except KeyboardInterrupt:
    pass 

GPIO.cleanup()

