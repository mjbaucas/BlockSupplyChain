from flask import Blueprint, request, jsonify
import json
from datetime import datetime

from database.models import RfidData, TempHumidData, AccelData, MotionData, PrivateBlockData
from database.managers import PrivateBlockchainManager

priv_db_mngr = PrivateBlockchainManager(PrivateBlockData)
private = Blueprint("private", __name__)

@private.route('/rfid-data/send', methods=['POST'])
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

@private.route('/temp-humid-data/send', methods=['POST'])
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

@private.route('/accel-data/send', methods=['POST'])
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

@private.route('/motion-data/send', methods=['POST'])
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

@private.route('/user/add', methods=['POST'])
def add_user():
	response = json.loads(request.get_json())
	if priv_db_mngr.add_user(response['user'], response['password'], response['secret']):
		return "SUCCESS: User successfully created!", 200
	return "FAILED: User already exists!", 500

@private.route('/user', methods=['GET'])
def print_users():
	return jsonify(priv_db_mngr.get_users()), 200