import requests
import json
from datetime import datetime
import time
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
PIR_PIN = 4
GPIO.setup(PIR_PIN, GPIO.IN)

device_id = "test_motion_device_01"
password = "password1234"

global_start = time.time()
time_limit = 600

url = 'http://' + sys.argv[1] + ':3000/motion-data/send'

total = 0
counter = 0

try:
    while True: 
        try:
            motion = 1 if GPIO.input(PIR_PIN) else 0
            print(motion)
            timestamp = datetime.now().timestamp()
            packet = {"credentials":{"userid": device_id, "password": password}, "data": {"motion": motion, "timestamp": timestamp}}
            temp_value = requests.post(url, json=json.dumps(packet), headers={'Content-Type': 'application/json', 'X-Api-Key': ''})
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
        time.sleep(2)
except KeyboardInterrupt:
    print('average:' + str(float(total/counter)))
    pass
