from threat import app
from threat import db,app
from threat import db,app,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return Register.query.get(int(id))


class Register(db.Model, UserMixin):
    
    id=db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    usertype = db.Column(db.String(80))
    name = db.Column(db.String(80))
    contact = db.Column(db.String(80))
    address = db.Column(db.String(80))
    status = db.Column(db.String(80),default='NULL')



class Prediction(db.Model, UserMixin):
    
    id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80))
    result = db.Column(db.String(80))
    det_date = db.Column(db.String(80))
    time = db.Column(db.String(80))


class Email(db.Model, UserMixin):
    
    id=db.Column(db.Integer, primary_key=True)
    det_date = db.Column(db.String(80))
    time = db.Column(db.String(80))
    