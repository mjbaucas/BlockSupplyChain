from flask import Flask, render_template, request
import json
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def display_page():
	return render_play('index.html')

if __name__=="__main__":
	app.run(host='0.0.0.0', threaded=True, port=3000)
