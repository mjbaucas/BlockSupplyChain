import sys
import time
import socket
import os

import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
gpio = 24

try:
    while True:
        try:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
            if humidity is not None and temperature is not None:      
                route = sys.argv[1]
                start = time.time()
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((route, 5000))
                client.send(str.encode(str(humidity) + " " + str(temperature)))
                print('time taken: ' + str((time.time()-start)*1000) + ' ms')
        except Exception as e:
            print(e)
        time.sleep(2)
except KeyboardInterrupt:
    pass

client.shutdown(socket.SHUT_RDWR)
client.close()
GPIO.cleanup()

