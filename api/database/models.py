from .db import db

class RfidData(db.Document):
    device = db.StringField(required=True)
    tag = db.StringField()
    timestamp = db.ComplexDateTimeField()