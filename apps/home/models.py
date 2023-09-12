from apps import db
from apps.authentication.models import Users
from datetime import datetime

class Bill(db.Model):

    __tablename__ = 'bill'

    id = db.Column(db.Integer, primary_key= True)
    value = db.Column(db.Float, nullable = False)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    payed = db.Column(db.Boolean, default = False)
    payed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return str(self.value) + ' at ' + self.timestamp.strftime("%m/%d/%Y, %H:%M:%S")