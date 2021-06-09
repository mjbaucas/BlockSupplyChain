from flask import Flask, render_template, request, jsonify
import json
import time

from database.db import initialize_db
from database.models import RfidData

from datetime import datetime, timezone
from dateutil import tz 

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': 'localhost',
    'port': 27017
}
db = initialize_db(app)

# Temporary data
temp_rfid = {}
rfid_counter = 0
temp_th = {}
th_counter = 0

# Temporary ledger for credentials
temp_ledger = {"test_rfid_device_01": "password1234", "test_temphumid_device_01": "password1234"}

# Detect local time
from_zone = tz.tzutc()
to_zone = tz.tzlocal()

# App utils
def check_user(userid, password):
	if userid in temp_ledger and temp_ledger[userid] == password:
		return True
	return False

def convert_utc_to_local(utc):
	utc = datetime.fromtimestamp(utc/1000, tz=from_zone)
	return utc.replace(tzinfo=from_zone).astimezone(to_zone).strftime("%Y-%m-%d %H:%M:%S")

def process_date(items):
	temp_date_list = convert_utc_to_local(items[-1]).split(" ")
	items[-1] = temp_date_list[0]
	items.append(temp_date_list[1])
	return items

def shortlist(data, length):
	temp = {}
	need_to_pop = len(data) - length
	if need_to_pop > 0:
		for i in range(1,length):
			temp[i] = data[i + need_to_pop]
		data = temp
	return data

@app.route('/', methods=['GET'])
def display_page():
	return render_template('index.html', rfid_data=temp_rfid, th_data=temp_th)

@app.route('/rfid-data', methods=['GET'])
def get_rfid_data():
	data = json.loads(RfidData.objects().to_json())
	return jsonify(data)

@app.route('/send/rfid', methods=['POST'])
def send_rfid_data():
	global rfid_counter
	global temp_rfid

	response = json.loads(request.get_json())
	if all (k in ["credentials", "data"] for k in response) and len(response) == 2:
		credentials = response["credentials"]
		if check_user(credentials["userid"], credentials["password"]):
			data = RfidData()
			data.device = credentials["userid"]
			data.tag = str(response["data"][0])
			data.timestamp = float(response["data"][1])
			data.save()
			return "", 200
	return "", 500

@app.route('/send/temphumid', methods=['POST'])
def send_th_data():
	global th_counter
	global temp_th

	response = json.loads(request.get_json())
	if all (k in ["credentials", "data"] for k in response) and len(response) == 2:
		credentials = response["credentials"]
		if check_user(credentials["userid"], credentials["password"]):
			th_counter+=1
			temp_th.update({rfid_counter: process_date(response["data"])})
			temp_th = shortlist(temp_th ,20)
			return "", 200
	return "", 500 

if __name__=="__main__":
	app.run(host='0.0.0.0', threaded=True, port=3000)
