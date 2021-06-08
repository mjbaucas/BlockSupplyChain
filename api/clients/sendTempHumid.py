import requests
import json
import time
import sys
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
gpio = 24

device_id = "test_temphumid_device_01"
password = "password1234"

url = 'http://' + sys.argv[1] + ':3000/send/temphumid'

try:
    while True: 
        try:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
            if humidity is not None and temperature is not None:                        
                print("Humidity: " + str(humidity) + " Temp: " + str(temperature))
                timestamp = int(round(time.time() * 1000))
                packet = {"credentials":{"userid": device_id, "password": password}, "data": [humidity, temperature, timestamp]}
                temp_value = requests.post(url, json=json.dumps(packet), headers={'Content-Type': 'application/json', 'X-Api-Key': ''})
        except Exception as e:
            #print(e) # Uncomment for debugging  
            pass
        time.sleep(5)
except KeyboardInterrupt:
    pass

    
