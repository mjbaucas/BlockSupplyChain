import time
import board
import adafruit_adxl34x



while True:


import requests
import json
from datetime import datetime
import time
import sys
import time
import board
import adafruit_adxl34x


i2c = board.I2C()
accelerometer = adafruit_adxl34x.ADXL345(i2c)

device_id = "test_accel_device_01"
password = "password1234"

url = 'http://' + sys.argv[1] + ':3000/send/accel'

try:
    while True: 
        try:
            axis_data = accelerometer.acceleration
            print("X: " + str(axis_data[0]) + " Y: " + str(axis_data[1]) + " Z: " + str(axis_data[2]))
            timestamp = datetime.now().timestamp()
            packet = {"credentials":{"userid": device_id, "password": password}, "data": {"x": axis_data[0], "y": axis_data[1], "z": axis_data[2], "timestamp": timestamp}}
            temp_value = requests.post(url, json=json.dumps(packet), headers={'Content-Type': 'application/json', 'X-Api-Key': ''})
        except Exception as e:
            #print(e) # Uncomment for debugging  
            pass
        time.sleep(5)
except KeyboardInterrupt:
    pass
