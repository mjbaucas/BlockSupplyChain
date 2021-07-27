# General imports
from flask import Flask, render_template
import json

# Database
from database.db import initialize_db
from database.models import RfidData, TempHumidData, AccelData, MotionData

# Main app definitions
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': 'localhost',
    'port': 27017
}
db = initialize_db(app)

# Blueprints
from private import private
from public import public

# Register blueprints
app.register_blueprint(private, url_prefix="/private")
app.register_blueprint(public, url_prefix="/public")

# App utils
def pretty_date(data):
	temp_data = []
	for item in data:
		temp_split = item["timestamp"].split(',')
		item["timestamp"] = f"{temp_split[0]}-{temp_split[1]}-{temp_split[2]} {temp_split[3]}:{temp_split[4]}:{temp_split[5]}.{temp_split[6]}"
		temp_data.append(item)
	return temp_data

# General routes
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

if __name__=="__main__":
	app.run(host='0.0.0.0', threaded=True, port=3000)
