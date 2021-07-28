from flask import Blueprint, request, jsonify
import json
from datetime import datetime

from database.models import RfidData, TempHumidData, AccelData, MotionData, PublicBlockData, PendingPublicBlockData
from database.managers import PublicBlockchainManager

pub_db_mngr = PublicBlockchainManager(PublicBlockData, PendingPublicBlockData, 3, 10)
public = Blueprint("public", __name__)

@public.route('/rfid-data/send', methods=['POST'])
def send_rfid_data():
	response = json.loads(request.get_json())
	if all (k in ["credentials", "data"] for k in response) and len(response) == 2:
		credentials = response["credentials"]
		if pub_db_mngr.check_participant(credentials["userid"]):
			pub_db_mngr.add_data_transaction({"device": credentials["userid"], "tag": str(response["data"]["tag"]), "timestamp": response["data"]["timestamp"]}, "rfid")
			block = pub_db_mngr.check_status(1)
			if block is not None:
				block_dict = pub_db_mngr.pending_model_to_dict(block["_id"]["$oid"])
				pub_db_mngr.add_block_to_chain()
				return jsonify({"block": block_dict, "difficulty": pub_db_mngr.difficulty, "block_id": block["_id"]["$oid"]}), 200
			else:
				return "", 300
	return "", 500

@public.route('/temp-humid-data/send', methods=['POST'])
def send_th_data():
	response = json.loads(request.get_json())
	if all (k in ["credentials", "data"] for k in response) and len(response) == 2:
		credentials = response["credentials"]
		if pub_db_mngr.check_participant(credentials["userid"]):
			pub_db_mngr.add_data_transaction({"device": credentials["userid"], "temperature": response["data"]["temperature"], "humidity": response["data"]["humidity"], "timestamp": response["data"]["timestamp"]}, "temp_humid")
			block = pub_db_mngr.check_status(1)
			if block is not None:
				block_dict = pub_db_mngr.pending_model_to_dict(block["_id"]["$oid"])
				pub_db_mngr.add_block_to_chain()
				return jsonify({"block": block_dict, "difficulty": pub_db_mngr.difficulty, "block_id": block["_id"]["$oid"]}), 200
			else:
				return "", 300
	return "", 500 

@public.route('/accel-data/send', methods=['POST'])
def send_accel_data():
	response = json.loads(request.get_json())
	if all (k in ["credentials", "data"] for k in response) and len(response) == 2:
		credentials = response["credentials"]
		if pub_db_mngr.check_participant(credentials["userid"]):
			pub_db_mngr.add_data_transaction({"device": credentials["userid"], "x": response["data"]["x"], "y": response["data"]["y"], "z": response["data"]["z"], "timestamp": response["data"]["timestamp"]}, "accel")
			block = pub_db_mngr.check_status(1)
			if block is not None:
				block_dict = pub_db_mngr.pending_model_to_dict(block["_id"]["$oid"])
				pub_db_mngr.add_block_to_chain()
				return jsonify({"block": block_dict, "difficulty": pub_db_mngr.difficulty, "block_id": block["_id"]["$oid"]}), 200
			else:
				return "", 300
	return "", 500 

@public.route('/motion-data/send', methods=['POST'])
def send_motion_data():
	response = json.loads(request.get_json())
	if all (k in ["credentials", "data"] for k in response) and len(response) == 2:
		credentials = response["credentials"]
		if pub_db_mngr.check_participant(credentials["userid"]):
			pub_db_mngr.add_data_transaction({"device": credentials["userid"], "motion": response["data"]["motion"], "timestamp": response["data"]["timestamp"]}, "motion")
			block = pub_db_mngr.check_status(1)
			if block is not None:
				block_dict = pub_db_mngr.pending_model_to_dict(block["_id"]["$oid"])
				pub_db_mngr.add_block_to_chain()
				return jsonify({"block": block_dict, "difficulty": pub_db_mngr.difficulty, "block_id": block["_id"]["$oid"]}), 200
			else:
				return "", 300
	return "", 500 

@public.route('/participant/register', methods=['POST'])
def register_participant():
	response = json.loads(request.get_json())
	key = pub_db_mngr.add_participant(response["userid"])
	if key is not None:
		return jsonify({"hashed_key": key}), 200
	else:
		return jsonify({"hashed_key": None}), 500

@public.route('/participant/proof', methods=['POST'])
def recieve_proof():
	response = json.loads(request.get_json())
	if all (k in ["credentials", "data"] for k in response) and len(response) == 2:
		credentials = response["credentials"]
		if pub_db_mngr.check_participant(credentials["userid"]):
			if pub_db_mngr.verify_proof_of_work(response["data"]["block_id"], response["data"]["proof_of_work"]):
				pub_db_mngr.vote_to_add_block(id = response["data"]["block_id"])
				return "", 200
			return "", 400
		return "", 300
	return "", 500

@public.route('/', methods=['GET'])
def test():
    return jsonify(pub_db_mngr.get_pending_blocks()), 200