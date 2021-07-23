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

global_start = time.time()
time_limit = 300

url = 'http://' + sys.argv[1] + ':3000/rfid-data/send'

total = 0
counter = 0

try:
    while True:
        try:
            tag, text = reader.read()
            #print(id)
            #print(text)
            timestamp = datetime.now().timestamp()
            packet = {"credentials":{"userid": device_id, "password": password}, "data": {"tag": tag, "timestamp": timestamp}}
            temp_value = requests.post(url, json=json.dumps(packet), headers={'Content-Type': 'application/json', 'X-Api-Key' : ''})
            elapsed = temp_value.elapsed.total_seconds()
            total+= elapsed
            counter+=1
            print('time taken: ' + str(elapsed))
            if time.time() > global_start + time_limit:
                print('average:' + str(float(total/counter)))
                break
        except Exception as e:
            #print(e) # Uncomment for debugging  
            pass
        #time.sleep(2)
except KeyboardInterrupt:
    print('average:' + str(float(total/counter)))
    pass

GPIO.cleanup()

