# General imports
import requests
import json
from datetime import datetime
import time
import sys
import hashlib

# Hardware specific
import board
import adafruit_adxl34x

i2c = board.I2C()
accelerometer = adafruit_adxl34x.ADXL345(i2c)

device_id = "test_accel_device_01"
blockchain_key = None
difficulty = 0

global_start = time.time()
time_limit = 300

register_participant_url = 'http://' + sys.argv[1] + ':3000/public/participant/register'
proof_of_work_url = 'http://' + sys.argv[1] + ':3000/public/participant/proof'
send_data_url = 'http://' + sys.argv[1] + ':3000/public/accel-data/send'

total = 0
counter = 0

def compute_hash(block):
    block_string = json.dumps(block, indent=4, sort_keys=True, default=str)
    return hashlib.sha256(block_string.encode()).hexdigest()

enabled = False
while blockchain_key is None and not enabled:
    packet = {"userid": device_id}
    temp_value = requests.post(register_participant_url, json=json.dumps(packet), headers={'Content-Type': 'application/json', 'X-Api-Key' : ''})
    if temp_value.status_code == 200:
        blockchain_key = temp_value.json()["hashed_key"]
        enabled = True

try:
    while True: 
        try:
            axis_data = accelerometer.acceleration
            print("X: " + str(axis_data[0]) + " Y: " + str(axis_data[1]) + " Z: " + str(axis_data[2]))
            timestamp = datetime.now().timestamp()
            packet = {"credentials":{"userid": blockchain_key}, "data": {"x": axis_data[0], "y": axis_data[1], "z": axis_data[2], "timestamp": timestamp}}
            temp_value = requests.post(send_data_url, json=json.dumps(packet), headers={'Content-Type': 'application/json', 'X-Api-Key': ''})
            if temp_value.status_code == 200:
                data = temp_value.json()
                block = data["block"]
                computed_hash = compute_hash(block)
                while not computed_hash.startswith('0' * data["difficulty"]):
                    block["nonce"] += 1
                    computed_hash = compute_hash(block)
                packet = {"credentials":{"userid": blockchain_key}, "data": {"proof_of_work": computed_hash, "block_id": data["block_id"]}}
                temp_value_2 = requests.post(proof_of_work_url, json=json.dumps(packet), headers={'Content-Type': 'application/json', 'X-Api-Key' : ''})
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
