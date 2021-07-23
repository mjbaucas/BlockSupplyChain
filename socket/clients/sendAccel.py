import sys
import time
from datetime import datetime
import socket
import os
import board
import adafruit_adxl34x
import json


i2c = board.I2C()
accelerometer = adafruit_adxl34x.ADXL345(i2c)

device_id = "test_accel_device_01"
password = "password1234"

global_start = time.time()
time_limit = 300

total = 0
counter = 0

try:
    while True:
        try:
            axis_data = accelerometer.acceleration
            route = sys.argv[1]
            start = time.time()
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((route, 5000))
            timestamp = datetime.now().timestamp()
            temp_dict = {'type': 'accel', 'user': device_id, 'password': password, 'data': {'x': axis_data[0], 'y': axis_data[1], 'z': axis_data[2]}, 'timestamp': timestamp}
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