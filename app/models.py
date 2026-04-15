# Add any model classes for Flask-SQLAlchemy here
from . import db
from werkzeug.security import generate_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    dob = db.Column(db.Date)
    looking_for = db.Column(db.String(128))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    gender = db.Column(db.String(128))
    
    def __init__(self, first_name, last_name, username, dob, looking_for, password, email, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.dob = dob
        self.looking_for = looking_for
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.email = email
        self.gender = gender
        

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
        
        