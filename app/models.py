# Add any model classes for Flask-SQLAlchemy here
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80),nullable=True)
    last_name = db.Column(db.String(80),nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=True)
    looking_for = db.Column(db.String(128),nullable=True) #Taking on and make a whole Prefernces tbale
    password = db.Column(db.String(128),nullable=True)
    email = db.Column(db.String(128),nullable=True)
    gender = db.Column(db.String(128),nullable=True)

    has_changed_dob = db.Column(db.Boolean, default=False) #Users can only change their DOB once 
    
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
        
    def update_dob(self, new_dob):
        if self.has_changed_dob:
            raise ValueError("DOB can only be updated once. Please contact support.")
        
        self.dob = new_dob
        self.has_changed_dob = True
        db.session.commit()
        
    def check_password(self, password_to_check):
        return check_password_hash(self.password, password_to_check)

    def set_password(self, new_password):
        self.password = generate_password_hash(new_password)
    

    def __repr__(self):
        return '<User %r>' % (self.username)
        

class Profile(db.Model):
    __tablename__ = 'profile'

    profile_id = db.Column(db.Integer, primary_key=True)
    # Ensure this ForeignKey matches your User table name (usually 'users.user_id')
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, unique=True)

    visibility = db.Column(db.String(50), nullable=False, default="Public") 
    preference = db.Column(db.String(50), nullable=True) 
    education = db.Column(db.String(50), nullable=True) 
    photo_url = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.String(255), nullable=True) 
    location = db.Column(db.String(100), nullable=True)

    # Relationship back to User
    user = db.relationship('User', backref=db.backref('profile', uselist=False))
    
    # Relationship for Interests (assuming interests_helper exists)
    interests = db.relationship('Interest', secondary=interests_helper, backref='profiles')

    def __init__(self, user_id, visibility="Public", preference=None, education=None, photo_url=None, bio=None, location=None):
        self.user_id = user_id 
        self.visibility = visibility
        self.preference = preference 
        self.education = education 
        self.photo_url = photo_url
        self.bio = bio
        self.location = location 

    @hybrid_property
    def dob(self):
        """Peeks at the DOB stored in the User model."""
        return self.user.dob if self.user else None

    @hybrid_property
    def age(self):
        """Calculates age based on the User's DOB."""
        if self.user and self.user.dob:
            today = date.today()
            dob = self.user.dob
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return None

    def update_profile(self, visibility=None, preference=None, education=None, photo_url=None, bio=None, location=None):
        """Updates profile fields and validates visibility."""
        allowed_options = ['Public', 'Private']
    
        if visibility is not None:
            if visibility in allowed_options:
                self.visibility = visibility
            else:
                raise ValueError(f"Invalid visibility. Choose from {allowed_options}")
        
        # Note: We removed 'dob' from here because it should be updated via the User model
        if preference:
            self.preference = preference 
        if education:
            self.education = education 
        if photo_url:
            self.photo_url = photo_url
        if bio:
            self.bio = bio
        if location:
            self.location = location
            
        db.session.commit()
        return self

    def __repr__(self):
        return f'<Profile {self.profile_id} for User {self.user_id}>'
    

class Interest(db.Model):

    pass 


# Preferences - Gender, Education, Religion, Age Range 