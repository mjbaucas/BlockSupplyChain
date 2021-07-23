import requests
import json
from datetime import datetime
import time
import sys
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
gpio = 24

device_id = "test_temphumid_device_01"
password = "password1234"

global_start = time.time()
time_limit = 600

url = 'http://' + sys.argv[1] + ':3000/temp-humid-data/send'

total = 0
counter = 0

try:
    while True: 
        try:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
            if humidity is not None and temperature is not None:                        
                print("Humidity: " + str(humidity) + " Temp: " + str(temperature))
                timestamp = datetime.now().timestamp()
                packet = {"credentials":{"userid": device_id, "password": password}, "data": {"humidity": humidity, "temperature": temperature, "timestamp": timestamp}}
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
    pass

    
