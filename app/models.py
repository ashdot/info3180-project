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
        
    likes_given = db.relationship('Like', foreign_keys=['Like.liker_id'], backref='author', lazy='dynamic')
    likes_received = db.relationship('Like', foreign_keys=['Like.liked_id'], backref='target', lazy='dynamic')

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
            db.session.delete(dislike_record)

    def dislike(self, profile):
        """
        Creates a new record in the Like table where action = dislike
        and match = False
    
        """
        new_like = Like(liker_id=self.user_id, liked_id=profile.user_id, is_match='False', action='dislike') 
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
            return str(self.user_id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)

        
class Like(db.Model):
    __tablename__ = 'like'
    
    like_id = db.Column(db.Integer, primary_key=True)
    liker_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False) 
    liked_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False) 
    created_at = db.Column(db.DateTime, default=db.func.now())
    is_match = db.Column(db.String(128))
    action = db.Column(db.String(128))
    
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
    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False) 
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.now())
 
    
    def __init__(self, sender_id, content, match_id):
        self.sender_id = sender_id
        self.content = content
        
    def get_message_id(self):
        try:
            return unicode(self.message_id)  # python 2 support
        except NameError:
            return str(self.message_id)  # python 3 support
        
        