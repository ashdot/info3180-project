# Add any model classes for Flask-SQLAlchemy here
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date, datetime, timezone

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80),nullable=True)
    last_name = db.Column(db.String(80),nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=True)

    looking_for = db.Column(db.String(128),nullable=True)

    password = db.Column(db.String(128),nullable=True)

    email = db.Column(db.String(128),nullable=True)

    gender = db.Column(db.String(128),nullable=True)

    has_changed_dob = db.Column(db.Boolean, default=False) #Users can only change their DOB once 
    

    notifications = db.relationship('Notification', backref='author', cascade="all, delete-orphan")

    """Created index on email and username for faster lookup"""
    __table_args__ = (
        db.Index('ix_user_email', 'email', unique=True),
        db.Index('ix_user_username', 'username', unique=True),
    )

    def __init__(self, first_name, last_name, username, dob, looking_for, password, email, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.dob = dob
        self.looking_for = looking_for
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.email = email
        self.gender = gender
        
    
    preferences = db.relationship('Preference', backref=db.backref('user', uselist=False))
        
    #likes_given = db.relationship('Like', foreign_keys=['Like.liker_id'], backref='author', lazy='dynamic')
    #likes_received = db.relationship('Like', foreign_keys=['Like.liked_id'], backref='target', lazy='dynamic')

    def like(self, profile):
        """
        Creates a new record in the Like table where action = like
        and is_match = maybe
        """
        if not self.has_liked(profile):
            new_like = Like(liker_id=self.user_id, liked_id=profile.user_id, is_match='Maybe', action='like')
            db.session.add(new_like)
        
    def remove_like(self, profile):
        like_record = Like.query.filter_by(
        liker_id=self.user_id, 
        liked_id=profile.user_id, 
        action='like').first()
        if like_record:
            db.session.delete(like_record)

    def dislike(self, profile):
        """
        Creates a new record in the Like table where action = dislike
        and match = False
    
        """
        new_like = Like(liker_id=self.user_id, liked_id=profile.user_id, is_match='No', action='dislike') 
        db.session.add(new_like)
        
    def remove_dislike(self, profile):
        dislike_record = Like.query.filter_by(
        liker_id=self.user_id, 
        liked_id=profile.user_id, 
        action='dislike').first()
    
        if dislike_record:
            db.session.delete(dislike_record)
        
    def has_disliked(self, profile):
        # Check if a like already exists
        return Like.query.filter_by(liker_id=self.user_id, liked_id=profile.user_id, action='dislike').first() is not None
    
    def has_liked(self, profile):
        # Check if a like already exists
        return Like.query.filter_by(liker_id=self.user_id, liked_id=profile.user_id, action='like').first() is not None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.user_id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support
        
    def update_dob(self, new_dob):
        """
        Ensures Dob is only updated once 
        """
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

    def __init__(self, user_id, visibility="Public", interests= None, education=None, photo_url=None, bio=None, location=None):
        self.user_id = user_id 
        self.visibility = visibility
        self.interests = interests
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

    def update_profile(self, visibility=None, interests=None, education=None, 
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

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    # Gender Preference (e.g., 'Male', 'Female', 'Non-binary', 'Everyone')
    gender_pref = db.Column(db.String(50), nullable=True)

    # Education level (e.g., 'High School', 'Bachelors', 'Masters', 'PhD')
    education_pref = db.Column(db.String(100), nullable=True)

    # Religion (e.g., 'Christian', 'Muslim', 'Atheist', 'Open')
    religion_pref = db.Column(db.String(100), nullable=True)

    # Age Range
    age_min = db.Column(db.Integer, default=18)
    age_max = db.Column(db.Integer, default=99)
    
    def __init__(self, user_id, gender_pref=None, education_pref=None, religion_pref=None, age_min=18, age_max=99):
        self.user_id = user_id
        self.gender_pref = gender_pref
        self.education_pref = education_pref
        self.religion_pref = religion_pref
        self.age_min = age_min
        self.age_max = age_max

    def __repr__(self):
        return f'<Preference User:{self.user_id} Age:{self.age_min}-{self.age_max}>'


class Like(db.Model):
    __tablename__ = 'like'
    
    like_id = db.Column(db.Integer, primary_key=True)
    liker_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False) 
    liked_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False) 
    created_at = db.Column(db.DateTime, default=db.func.now())
    is_match = db.Column(db.String(128))
    action = db.Column(db.String(128))

    __table_args__ = (
        # Creates a index for faster like retrival and ensures no duplicate likes 
        db.Index('ix_unique_like_direction', 'liker_id', 'liked_id', unique=True),
    )
    
    def __init__(self, liker_id, liked_id, is_match, action):
        self.liker_id = liker_id
        self.liked_id = liked_id
        self.is_match = is_match
        self.action = action
        
    def get_like_id(self):
        try:
            return unicode(self.like_id)  # python 2 support
        except NameError:
            return str(self.like_id)  # python 3 support

class Match(db.Model):
    __tablename__ = 'matches'
    
    match_id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False) 
    user2_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False) 
    matched_at = db.Column(db.DateTime, default=db.func.now())


    __table_args__ = (
        # Creates an index on matches users for faster match retrival 
        db.Index('ix_match_user_pair', 'user1_id', 'user2_id'),
    )
    
    def __init__(self, user1_id, user2_id):
        self.user1_id = user1_id
        self.user2_id = user2_id
        #find a way to ensure that no duplicates are entered.


        
    def get_match_id(self):
        try:
            return unicode(self.match_id)  # python 2 support
        except NameError:
            return str(self.match_id)  # python 3 support
        

class Message(db.Model):
    __tablename__ = 'messages'

    message_id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.match_id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(
        db.DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')
    match = db.relationship('Match', backref=db.backref('messages', lazy='dynamic'))
    
    def __init__(self, match_id, sender_id, receiver_id, content):
        self.match_id = match_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content

    def __repr__(self):
        return f'<Message from {self.sender_id} to {self.receiver_id} at {self.timestamp}>'
    
    

class SavedProfile(db.Model):
    __tablename__ = 'saved_profiles'

    id = db.Column(db.Integer, primary_key=True)
    saver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    saved_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    # Ensure a user can't save the same person twice
    __table_args__ = (db.UniqueConstraint('saver_id', 'saved_id', name='_saver_saved_uc'),)


class Notification(db.Model):
    __tablename__ = 'notifications'

    notif_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    # Linkage to the User Table 
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False) 