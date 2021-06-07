from flask import Flask, render_template, request
import json
import time

app = Flask(__name__)

temp = {}

temp_ledger = {"test_rfid_device_01": "password1234"}

@app.route('/', methods=['GET'])
def display_page():
	return render_template('index.html', rfid_data=temp)

@app.route('/send_rfid', methods=['POST'])
def send_data():
	response = json.loads(request.get_json())
	print(response)
	if all (k in ["credentials", "data"] for k in response) and len(response) == 2:
		credentials = response["credentials"]
		if check_user(credentials["userid"], credentials["password"]):
			temp.update(data)
			return "", 200
	return "", 500

if __name__=="__main__":
	app.run(host='0.0.0.0', threaded=True, port=3000)

def check_user(userid, password):
	if userid in temp_ledger and temp_ledger[userid] == password:
		return True
	return False