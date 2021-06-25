from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import time

from database.db import initialize_db
from database.models import RfidData, TempHumidData, AccelData

from datetime import datetime, timezone
from dateutil import tz 

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': 'localhost',
    'port': 27017
}
db = initialize_db(app)

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

def pretty_date(data):
	temp_data = []
	for item in data:
		temp_split = item["timestamp"].split(',')
		item["timestamp"] = f"{temp_split[0]}-{temp_split[1]}-{temp_split[2]} {temp_split[3]}:{temp_split[4]}:{temp_split[5]}.{temp_split[6]}"
		temp_data.append(item)
	return temp_data

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
	rfid = json.loads(RfidData.objects().order_by('-timestamp').limit(10).to_json())
	rfid = pretty_date(rfid)
	temp_humid = json.loads(TempHumidData.objects().order_by('-timestamp').limit(10).to_json())
	temp_humid = pretty_date(temp_humid)
	return render_template('index.html', rfid_data=rfid, th_data=temp_humid)

@app.route('/rfid-data', methods=['GET'])
def get_rfid_data():
	data = json.loads(RfidData.objects().order_by('-timestamp').limit(10).to_json())
	return jsonify(data)

@app.route('/send/rfid', methods=['POST'])
def send_rfid_data():
	response = json.loads(request.get_json())
	if all (k in ["credentials", "data"] for k in response) and len(response) == 2:
		credentials = response["credentials"]
		if check_user(credentials["userid"], credentials["password"]):
			data = RfidData()
			data.device = credentials["userid"]
			data.tag = str(response["data"]["tag"])
			data.timestamp = datetime.fromtimestamp(response["data"]["timestamp"])
			data.save()
			return "", 200
	return "", 500

@app.route('/send/temp-humid', methods=['POST'])
def send_th_data():
	response = json.loads(request.get_json())
	if all (k in ["credentials", "data"] for k in response) and len(response) == 2:
		credentials = response["credentials"]
		if check_user(credentials["userid"], credentials["password"]):
			data = TempHumidData()
			data.device = credentials["userid"]
			data.temperature = response["data"]["temperature"]
			data.humidity = response["data"]["humidity"]
			data.timestamp = datetime.fromtimestamp(response["data"]["timestamp"])
			data.save()
			return "", 200
	return "", 500 

@app.route('/send/accel', methods=['POST'])
def send_accel_data():
	response = json.loads(request.get_json())
	if all (k in ["credentials", "data"] for k in response) and len(response) == 2:
		credentials = response["credentials"]
		if check_user(credentials["userid"], credentials["password"]):
			data = AccelData()
			data.device = credentials["userid"]
			data.temperature = response["data"]["x"]
			data.humidity = response["data"]["y"]
			data.humidity = response["data"]["z"]
			data.timestamp = datetime.fromtimestamp(response["data"]["timestamp"])
			data.save()
			return "", 200
	return "", 500 

if __name__=="__main__":
	app.run(host='0.0.0.0', threaded=True, port=3000)
