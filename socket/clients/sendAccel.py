import sys
import time
import socket
import os
import board
import adafruit_adxl34x


i2c = board.I2C()
accelerometer = adafruit_adxl34x.ADXL345(i2c)

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
            client.send(str.encode(str(axis_data[0]) + " " +  str(axis_data[1]) + " " + str(axis_data[2])))
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