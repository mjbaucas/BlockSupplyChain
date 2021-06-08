from flask import Flask, render_template, request
import json
import time

from datetime import datetime, timezone
from dateutil import tz 

app = Flask(__name__)

# Holds all RFID data
temp = {}
counter = 0

# Temporary ledger for credentials
temp_ledger = {"test_rfid_device_01": "password1234"}

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

def process_dates(dates):
	for key in dates.keys():
		temp_date_list = convert_utc_to_local(dates[key][1]).split(" ")
		dates[key][1] = temp_date_list[0]
		dates[key].append(temp_date_list[1])
	return dates


@app.route('/', methods=['GET'])
def display_page():
	return render_template('index.html', rfid_data=temp)

@app.route('/send_rfid', methods=['POST'])
def send_data():
	response = json.loads(request.get_json())
	if all (k in ["credentials", "data"] for k in response) and len(response) == 2:
		credentials = response["credentials"]
		if check_user(credentials["userid"], credentials["password"]):
			counter+=1
			temp.update({counter: process_date(response["data"])})
			return "", 200
	return "", 500

if __name__=="__main__":
	app.run(host='0.0.0.0', threaded=True, port=3000)

