from .db import db

class RfidData(db.Document):
    device = db.StringField(required=True)
    tag = db.StringField()
    timestamp = db.ComplexDateTimeField()

class TempHumidData(db.Document):
    device = db.StringField(required=True)
    temperature = db.FloatField()
    humidity = db.FloatField()
    timestamp = db.ComplexDateTimeField()

class AccelData(db.Document):
    device = db.StringField(required=True)
    x = db.FloatField()
    y = db.FloatField()
    z = db.FloatField()
    timestamp = db.ComplexDateTimeField()

class MotionData(db.Document):
    device = db.StringField(required=True)
    timestamp = db.ComplexDateTimeField()