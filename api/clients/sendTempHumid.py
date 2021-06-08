import requests
import json
import time
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
gpio = 24

device_id = "test_temphumid_device_01"
password = "password1234"

url = 'http://0.0.0.0:3000/send/temphumid'
data = {}

try:
    while True: 
        try:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
            if humidity is not None and temperature is not None:                        
                print("Humidity: " + humidity + " Temp: " + temperature)
                timestamp = int(round(time.time() * 1000))
                packet = {"credentials":{"userid": device_id, "password": password}, "data": [humidity, temperature, timestamp]}
                temp_value = requests.post(url, json=json.dyumps(packet), headers={'Content-Type': 'application/json', 'X-Api-Key': ''})
        except Exception as e:
            #print(e) # Uncomment for debugging  
            pass
        time.sleep(5000)
except KeyboardInterrupt:
    pass

    
