import sys
import time
import socket
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
PIR_PIN = 4
GPIO.setup(PIR_PIN, GPIO.IN)

total = 0
counter = 0

try:
    while True:
        try:
            if GPIO.input(PIR_PIN):
                route = sys.argv[1]
                start = time.time()
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((route, 5000))
                client.send(str.encode('motion'))
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
GPIO.cleanup()
