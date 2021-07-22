import sys
import time
import socket
import os
import board
import adafruit_adxl34x
import json


i2c = board.I2C()
accelerometer = adafruit_adxl34x.ADXL345(i2c)

device_id = "test_accel_device_01"
password = "password1234"

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
            temp_dict = {'user': device_id, 'password': password, 'data': {'x': axis_data[0], 'y': axis_data[1], 'z': axis_data[2]}}
            client.send(str.encode(json.dumps(temp_dict)))
            elapsed = (time.time()-start)*1000
            total+= elapsed
            counter+=1
            print('time taken: ' + str(elapsed) + ' ms')
        except Exception as e:
            print(e)
        time.sleep(2)
except KeyboardInterrupt:
    print('average:' + str(float(total/counter)))
    pass

client.shutdown(socket.SHUT_RDWR)
client.close()