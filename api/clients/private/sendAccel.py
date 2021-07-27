# General imports
import requests
import json
from datetime import datetime
import time
import sys

# Hardware specific
import board
import adafruit_adxl34x


i2c = board.I2C()
accelerometer = adafruit_adxl34x.ADXL345(i2c)

device_id = "test_accel_device_01"
password = "password1234"

global_start = time.time()
time_limit = 300

url = 'http://' + sys.argv[1] + ':3000/private/accel-data/send'

total = 0
counter = 0

try:
    while True: 
        try:
            axis_data = accelerometer.acceleration
            print("X: " + str(axis_data[0]) + " Y: " + str(axis_data[1]) + " Z: " + str(axis_data[2]))
            timestamp = datetime.now().timestamp()
            packet = {"credentials":{"userid": device_id, "password": password}, "data": {"x": axis_data[0], "y": axis_data[1], "z": axis_data[2], "timestamp": timestamp}}
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
        #time.sleep(2)
except KeyboardInterrupt:
    print('average:' + str(float(total/counter)))
    pass
