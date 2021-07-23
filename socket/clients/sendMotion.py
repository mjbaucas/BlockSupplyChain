import sys
import time
from datetime import datetime
import socket
import os
import RPi.GPIO as GPIO
import json

GPIO.setmode(GPIO.BCM)
PIR_PIN = 4
GPIO.setup(PIR_PIN, GPIO.IN)

device_id = "test_motion_device_01"
password = "password1234"

global_start = time.time()
time_limit = 300

total = 0
counter = 0

try:
    while True:
        try:
            motion = 1 if GPIO.input(PIR_PIN) else 0
            print(motion)
            route = sys.argv[1]
            start = time.time()
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((route, 5000))
            timestamp = datetime.now().timestamp()
            temp_dict = {'type': 'motion', 'user': device_id, 'password': password, 'data':motion, 'timestamp': timestamp}
            client.send(str.encode(json.dumps(temp_dict)))
            elapsed = (time.time()-start)*1000
            total+= elapsed
            counter+=1
            print('time taken: ' + str(elapsed) + ' ms')
            if time.time() > global_start + time_limit:
                print('average:' + str(float(total/counter)))
                break
        except Exception as e:
            print(e)
        #time.sleep(2)
except KeyboardInterrupt:
    print('average:' + str(float(total/counter)))
    pass

client.shutdown(socket.SHUT_RDWR)
client.close()
GPIO.cleanup()
