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
    motion = db.IntField()
    timestamp = db.ComplexDateTimeField()

class PrivateBlockData(db.Document):
    previous_hash = db.StringField(required=True, unique=True)
    timestamp = db.ComplexDateTimeField(required=True)
    nonce = db.IntField(required=True)
    transactions = db.ListField(field=db.StringField())
    current_level = db.IntField(required=True)
    