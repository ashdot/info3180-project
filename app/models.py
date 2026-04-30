# Add any model classes for Flask-SQLAlchemy here
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date, datetime

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80),nullable=True)
    last_name = db.Column(db.String(80),nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=True)

    #should be Casual, Serious, Friendship or smt lke that 
    looking_for = db.Column(db.String(128),nullable=True) 

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, unique=True)
    visibility = db.Column(db.String(50), nullable=False, default="Public") 
    preference = db.Column(db.String(50), nullable=True) 
    education = db.Column(db.String(50), nullable=True) 
    photo_url = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.String(255), nullable=True) 
    location = db.Column(db.String(100), nullable=True)

    interests = db.Column(db.String(255), nullable=True)

    PERSONAL_INTERESTS = [
    'Tech', 'Music', 'Art', 'Sports', 'Cooking', 'Travel',
    'Fitness', 'Gaming', 'Reading', 'Film', 
    'Photography', 'Fashion', 'Pets', 'Socializing']

    # Relationship back to User
    user = db.relationship('User', backref=db.backref('profile', uselist=False))

    def __init__(self, user_id, visibility="Public", interests= None, preference=None, education=None, photo_url=None, bio=None, location=None):
        self.user_id = user_id 
        self.visibility = visibility
        self.interests = interests
        self.preference = preference 
        self.education = education 
        self.photo_url = photo_url
        self.bio = bio
        self.location = location 

    @hybrid_property
    def looking_for(self):
        """Peeks at looking_for stored in the User model."""
        return self.user.looking_for if self.user else None

    @looking_for.setter
    def looking_for(self, value):
        """Updates looking_for in the User model when set on the Profile."""
        if self.user:
            self.user.looking_for = value

    @hybrid_property
    def dob(self):
        return self.user.dob if self.user else None

    @hybrid_property
    def age(self):
        if self.user and self.user.dob:
            today = date.today()
            dob = self.user.dob
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return None

    def update_profile(self, visibility=None, interests=None, preference=None, education=None, 
                       photo_url=None, bio=None, location=None, looking_for=None):
        """Updates profile fields and associated user fields."""
        allowed_options = ['Public', 'Private']
    
        if visibility is not None:
            if visibility in allowed_options:
                self.visibility = visibility
            else:
                raise ValueError(f"Invalid visibility. Choose from {allowed_options}")
            
       
        
        # Update User-level data through the setter
        if looking_for is not None:
            self.looking_for = looking_for

        if interests:
            self.interests = interests

        # Update Profile-level data
        if preference: #Do we even need to display preferences on profiles
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
    


class Preference(db.Model):
    __tablename__ = 'preferences'

    pref_id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Gender Preference (e.g., 'Male', 'Female', 'Non-binary', 'Everyone')
    gender_pref = db.Column(db.String(50), nullable=True)

    # Education level (e.g., 'High School', 'Bachelors', 'Masters', 'PhD')
    education_pref = db.Column(db.String(100), nullable=True)

    # Religion (e.g., 'Christian', 'Muslim', 'Atheist', 'Open')
    religion_pref = db.Column(db.String(100), nullable=True)

    # Age Range

    #Ask Rochele abt this 

    age_min = db.Column(db.Integer, default=18)
    age_max = db.Column(db.Integer, default=99)

    def __repr__(self):
        return f'<Preference User:{self.user_id} Age:{self.age_min}-{self.age_max}>'


#d) Save favorite/bookmarked profiles -> class SavedProfiles(db.Model)





from datetime import datetime, timezone

class Messages(db.Model):
    __tablename__ = 'messages'

    message_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    timestamp = db.Column(
        db.DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')

    def __init__(self, sender_id, receiver_id, content):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content

    def __repr__(self):
        return f'<Message from {self.sender_id} to {self.receiver_id} at {self.timestamp}>'