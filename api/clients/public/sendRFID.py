# General imports
import requests
import json
from datetime import datetime
import time
import sys

# Hardware specific
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

device_id = "test_rfid_device_01"
blockchain_key = None

global_start = time.time()
time_limit = 300

register_participant_url = 'http://' + sys.argv[1] + ':3000/public/participant/register'
proof_of_work_url = 'http://' + sys.argv[1] + ':3000/public/participant/proof'
send_data_url = 'http://' + sys.argv[1] + ':3000/public/rfid-data/send'


total = 0
counter = 0

enabled = False
while blockchain_key is None and enabled = True:
    packet = {"credentials":{"userid": device_id}}
    temp_value = requests.post(register_participant_url, json=json.dumps(packet), headers={'Content-Type': 'application/json', 'X-Api-Key' : ''})
    if temp_value.status_code == 200:
        blockchain_key = temp_value.json["hashed_key"]
        enabled = True

try:
    while True:
        try:
            tag, text = reader.read()
            timestamp = datetime.now().timestamp()
            packet = {"credentials":{"userid": blockchain_key}, "data": {"tag": tag, "timestamp": timestamp}}
            temp_value = requests.post(send_data_url, json=json.dumps(packet), headers={'Content-Type': 'application/json', 'X-Api-Key' : ''})
            if temp_value.status_code == 200 and temp_value.json is not None and "block" in temp_value.json:
                block = temp_value.json["block"]
                computed_hash = self.compute_hash(block)
                while not computed_hash.startswith('0' * self.difficulty):
                    block["nonce"] += 1
                    computed_hash = self.compute_hash(block)
                packet = {"credentials":{"userid": device_id}, {"data": {"proof_of_work": computed_hash, "block_id": block["_id"]["$oid"]}}}
                temp_value = requests.post(proof_of_work_url, json=json.dumps(packet), headers={'Content-Type': 'application/json', 'X-Api-Key' : ''})
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

GPIO.cleanup()

