from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import time

from database.db import initialize_db
from database.models import RfidData, TempHumidData, AccelData, MotionData, PrivateBlockData
from database.managers import PrivateBlockchainManager

from datetime import datetime, timezone
from dateutil import tz 

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': 'localhost',
    'port': 27017
}
db = initialize_db(app)
priv_db_mngr = PrivateBlockchainManager(PrivateBlockData)

# Detect local time
from_zone = tz.tzutc()
to_zone = tz.tzlocal()

# App utils
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
	motion= json.loads(MotionData.objects().order_by('-timestamp').limit(10).to_json())
	motion = pretty_date(motion)
	accel = json.loads(AccelData.objects().order_by('-timestamp').limit(10).to_json())
	accel = pretty_date(accel)
	return render_template('index.html', rfid_data=rfid, th_data=temp_humid, motion_data=motion, accel_data=accel)

@app.route('/rfid-data', methods=['GET'])
def get_rfid_data():
	data = json.loads(RfidData.objects().order_by('-timestamp').limit(10).to_json())
	return jsonify(data)

@app.route('/rfid-data/send', methods=['POST'])
def send_rfid_data():
	response = json.loads(request.get_json())
	if all (k in ["credentials", "data"] for k in response) and len(response) == 2:
		credentials = response["credentials"]
		if priv_db_mngr.check_user(credentials["userid"], credentials["password"]):
			data = RfidData()
			data.device = credentials["userid"]
			data.tag = str(response["data"]["tag"])
			data.timestamp = datetime.fromtimestamp(response["data"]["timestamp"])
			data.save()
			return "", 200
	return "", 500

@app.route('/temp-humid-data/send', methods=['POST'])
def send_th_data():
	response = json.loads(request.get_json())
	if all (k in ["credentials", "data"] for k in response) and len(response) == 2:
		credentials = response["credentials"]
		if priv_db_mngr.check_user(credentials["userid"], credentials["password"]):
			data = TempHumidData()
			data.device = credentials["userid"]
			data.temperature = response["data"]["temperature"]
			data.humidity = response["data"]["humidity"]
			data.timestamp = datetime.fromtimestamp(response["data"]["timestamp"])
			data.save()
			return "", 200
	return "", 500 

@app.route('/accel-data/send', methods=['POST'])
def send_accel_data():
	response = json.loads(request.get_json())
	if all (k in ["credentials", "data"] for k in response) and len(response) == 2:
		credentials = response["credentials"]
		if priv_db_mngr.check_user(credentials["userid"], credentials["password"]):
			data = AccelData()
			data.device = credentials["userid"]
			data.x = response["data"]["x"]
			data.y = response["data"]["y"]
			data.z = response["data"]["z"]
			data.timestamp = datetime.fromtimestamp(response["data"]["timestamp"])
			data.save()
			return "", 200
	return "", 500 

@app.route('/motion-data/send', methods=['POST'])
def send_motion_data():
	response = json.loads(request.get_json())
	if all (k in ["credentials", "data"] for k in response) and len(response) == 2:
		credentials = response["credentials"]
		if priv_db_mngr.check_user(credentials["userid"], credentials["password"]):
			data = MotionData()
			data.device = credentials["userid"]
			data.motion = response["data"]["motion"]
			data.timestamp = datetime.fromtimestamp(response["data"]["timestamp"])
			data.save()
			return "", 200
	return "", 500 

@app.route('/user/add', methods=['POST'])
def add_user():
	response = json.loads(request.get_json())
	if priv_db_mngr.add_user(response['user'], response['password'], response['secret']):
		return "SUCCESS: User successfully created!", 200
	return "FAILED: User already exists!", 500

@app.route('/user', methods=['GET'])
def print_users():
	return jsonify(priv_db_mngr.get_users()), 200

if __name__=="__main__":
	app.run(host='0.0.0.0', threaded=True, port=3000)
