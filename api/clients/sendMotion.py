import requests
import json
from datetime import datetime
import time
import sys
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
PIR_PIN = 4
GPIO.setup(PIR_PIN, GPIO.IN)


device_id = "test_accel_device_01"
password = "password1234"

url = 'http://' + sys.argv[1] + ':3000/send/motion'

try:
    while True: 
        try:
            if GPIO.input(PIR_PIN):
                print("Motion Detected")
                timestamp = datetime.now().timestamp()
                packet = {"credentials":{"userid": device_id, "password": password}, "data": {"timestamp": timestamp}}
                temp_value = requests.post(url, json=json.dumps(packet), headers={'Content-Type': 'application/json', 'X-Api-Key': ''})
        except Exception as e:
            #print(e) # Uncomment for debugging  
            pass
        time.sleep(5)
except KeyboardInterrupt:
    pass
