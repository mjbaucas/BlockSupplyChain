from flask import Flask, render_template, request
import json
import time

app = Flask(__name__)

temp = {}

@app.route('/', methods=['GET'])
def display_page():
	return render_template('index.html', rfid_data=temp)

@app.route('/send_rfid', methods=['POST'])
def send_data():
	response = request.get_json()
	print(response)
	temp.update({"1": 123120321})
	return "", 200

if __name__=="__main__":
	app.run(host='0.0.0.0', threaded=True, port=3000)
