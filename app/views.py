"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os
from app import app
from . import db 
from app.models import User, Profile, Preference, Like, Match, Message
from .forms import LoginForm, SignUpForm, EditProfile, MessageForm
from flask import render_template, request, jsonify, send_file, flash, send_from_directory, url_for
from flask_login import login_user, logout_user, verify_password, current_user, login_required
from werkzeug.utils import secure_filename
from sqlalchemy import or_



###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/v1/auth/login', methods=['POST']) 
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing email or password"}), 400

    user = User.query.filter_by(email=data.get('email')).first()

 
    if user and user.check_password(data.get('password')):
        login_user(user, remember=True) 
        
        return jsonify({
            "message": "Login successful",
            "user": {
                "username": user.username,
                "first_name": user.first_name,
                "user_id": user.user_id
            }
        }), 200

    return jsonify({"error": "Invalid email or password"}), 401


@app.route('/api/v1/signup', methods=['POST'])
def signup():
    data = request.get_json() 
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({"error": "Email already exists"}), 400

    try:
        # Creates the User object
        new_user = User(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            username=data.get('username'),
            dob=data.get('dob'), 
            looking_for=data.get('looking_for', 'Casual'), # Provide a default if missing
            password=data.get('password'),
            email=data.get('email'),
            gender=data.get('gender')
        )
        
        db.session.add(new_user)
        # Flush sends the SQL to the DB so the user_id is generated
        db.session.flush() 

        #Creates the Profile object automatically
        new_profile = Profile(
            user_id=new_user.user_id, 
            visibility="Public", #Sets visibility of Profile to public automatically 
            education=None,
            photo_url=None,
            bio=None,
            location=None
        )
        
        db.session.add(new_profile)
        db.session.commit() 

        return jsonify({"message": f"Welcome to DriftDater {new_user.username}!"}), 201
        
    except Exception as e:
        db.session.rollback() 
        return jsonify({"error": str(e)}), 500
    



# List all user Profiles
@app.route('/api/v1/profile/all', methods=['GET'])
#@login_required 
def list_profile():

    # Query all profiles and join with User to avoid N+1 query issues
    profiles = Profile.query.all()
    
    result = []
    for p in profiles:
        result.append({
            "profile_id": p.profile_id,
            "user_id": p.user_id,
            "username": p.user.username if p.user else "Unknown",
            "full_name": f"{p.user.first_name} {p.user.last_name}" if p.user else "Unknown",
            "photo_url": p.photo_url,
            "location": p.location,
            "age": p.age,
            "interests": p.interests,
            "visibility": p.visibility
        })
        
    return jsonify({"status": "success", "profiles": result}), 200


# Gets a singular Profile when clicked on 
@app.route('/api/v1/profile/<int:user_id>', methods=['GET'])
#@login_required 
def single_profile(user_id):

    # We query by user_id since your route uses <user_id>
    profile = Profile.query.filter_by(user_id=user_id).first_or_404()
    
    return jsonify({
        "status": "success",
        "data": {
            "profile_id": profile.profile_id,
            "user_id": profile.user_id,
            "username": profile.user.username,
            "bio": profile.bio,
            "education": profile.education,
            "location": profile.location,
            "photo_url": profile.photo_url,
            "interests": profile.interests,
            "age": profile.age,
            "looking_for": profile.looking_for, # Using your hybrid property
            "visibility": profile.visibility
        }
    }), 200




#Displays current user's profile 
@app.route('/api/v1/profile', methods=['GET'])
#@login_required 
def display_profile():
    data = request.get_json()
    
    #Gets current user's profile
    profile = Profile.query.filter_by(username=current_user).first()

    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    current_age = profile.age 
    age_display = age_range(current_age)

    photo = url_for('get_photo', filename=profile.photo_url) if profile.photo_url else profile.photo_url

    return jsonify({
        "username": profile.user.username, 
        "first_name": profile.user.first_name,
        "age": age_display,
        "bio": profile.bio,
        "photo": photo,
        "location": profile.location,
        "gender": profile.gender,
        "looking_for": profile.looking_for,
        "interests": profile.interests
    }), 200


#Allows edits to be made to the current profile 
@app.route('/api/v1/profile/edit', methods=['PUT'])
#@login_required
def edit_profile():

    #Gets current user's profile
    profile = Profile.query.filter_by(user_id=current_user.user_id).first()

    data = request.form
    photo = request.files.get('photo')

    try:
        
        if data.get('bio') and len(data.get('bio')) > 255:
            return jsonify({"error": "Bio too long"}), 400

        
        if photo:
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile.photo_url = filename

        
        profile.update_profile(
            visibility=data.get('visibility'),
            education=data.get('education'),
            bio=data.get('bio'),
            location=data.get('location')
        )

        return jsonify({
            "message": "Profile updated successfully",
            "photo_url": profile.photo_url 
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



#Age range function to display on profile 
def age_range(age):

    age_ranges = {1: "18-20",2:"21-30", 3: "31-40", 4: "41-50", 5: "51-60", 6: "60+"}

    if age >= 18 and age <= 20:
        return age_ranges[1]
    if age >= 21 and age <= 30:
        return age_ranges[2]
    if age >= 31 and age <= 40:
        return age_ranges[3]
    if age >= 41 and age <= 50:
        return age_ranges[4]
    if age >= 51 and age <= 60:
        return age_ranges[5]
    if age > 60:
        return age_ranges[6]
        

@app.route('/api/v1/auth/logout')
#@login_required
def logout():

    # Clears the session cookie and logs the user out
    logout_user()
    
    return jsonify({
        "status": "success",
        "message": "See you later! Hope your next match is just a 'drift' away."
    }), 200


###
# Matching Algorithm
###

def calculate_match_score(user, candidate): #user is a dict put together in another function
    """
    Calculates a match score based on 4 categories.
    Categories: Location, Age, Interests and Gender
    """
    score = 0
    # Weights for each category (optional, adds precision)
    weights = {'location': 0.5, 'age': 1.5, 'interests': 0.5, 'gender': 1.5} 
        
    if candidate['location'] == user['location']:
        score += weights['location']
        
    min_age = user['age'][0]
    max_age = user['age'][1]
    if candidate['age'] >= min_age and candidate['age'] <= max_age: 
        score += weights['age'] 

    #Adds 0.5 to score for each matching interest.
    for i in candidate['interests']:
        if i in user['interests']: 
            score += weights['interests']
            
    if candidate['gender'] == user['gender'] or user['gender'] == 'Both':
        score += weights['gender']
        
    return score

@app.route('/api/v1/matches', methods = ['GET'])
@login_required
def display_matches(): 
    """
    Displays matched profiles to logged in users
    """
    user_id = current_user.id
    
    #remove all profiles the user has already viewed
    interacted = db.session.query(Like.liked_id).filter(Like.liker_id == user_id).all()
    interacted_ids = [i[0] for i in interacted] + [user_id]
    
    profiles = db.session.execute(db.select(Profile)).filter(~Profile.user_id.in_(interacted_ids)).scalars()
    
    user= db.session.execute(db.select(Profile).filter_by(user_id=user_id)).scalar_one() 
    
    scored_match_list = []
    for profile in profiles:
        candidate = {'location': profile.location, 'age': profile.age(), 'interests': profile.interests, 'gender': profile.user.gender}
        user = {'location': user.location, 'age': [user.preferences.age_min, user.preferences.age_max], 'interests': user.interests, 'gender': user.preferences.gender_pref}
        
        score = calculate_match_score(user, candidate)
        photo = url_for('get_photo', filename=profile.photo_url) if profile.photo_url else profile.photo_url

        scored_match_list.append({
            "id": profile.user_id,
            "photo": photo,
            "username": profile.user.username,
            "first_name": profile.user.first_name,
            "last_name": profile.user.last_name,
            "gender": profile.user.gender,
            "bio": profile.bio,
            "score": score
        })
    #top_50_matches = scored_match_list[:50]
    #return jsonify({"matches": top_50_matches, "total_available": len(scored_match_list)}), 200
    
    return jsonify({"matches": scored_match_list}), 200

@app.route('/api/v1/profiles/<id>/like', methods = ['POST'])
@login_required
def like_profile(id):
    """
    When users like a profile, the like is saved to the database.
    If the likes between the two users are mutual, 
    the system asks the user to confirm the match
    """
    profile_to_like = User.query.get_or_404(id)
    
    # Check if the user is trying to like themselves
    if current_user.id == profile_to_like.id:
        return jsonify({"error": "You cannot like your own profile"}), 400

    # remove like from database if user presses like again
    if current_user.has_liked(profile_to_like):
        current_user.remove_like(profile_to_like)

        #remove any match records if like is removed
        match_record = Match.query.filter(((Match.user1_id == current_user.user_id) & (Match.user2_id == profile_to_like.user_id))).first()
        match_record_rev = Match.query.filter(((Match.user1_id == profile_to_like.user_id) & (Match.user2_id == current_user.user_id))).first()
        if match_record:
            db.session.delete(match_record)
        if match_record_rev:
            db.session.delete(match_record_rev)
        
        db.session.commit()
        return jsonify({"message": "Like removed"}), 200
   
    # if the above cases are false, like the profile and add like record to database
    current_user.like(profile_to_like)
    db.session.commit()
    total_likes = profile_to_like.likes_received.count()
    
    is_mutual = profile_to_like.has_liked(current_user)
    
    #to be fixed
    if is_mutual:
        existing_match = Match.query.filter(
        or_(
            (Match.user1_id == current_user.user_id) & (Match.user2_id == profile_to_like.user_id),
            (Match.user1_id == profile_to_like.user_id) & (Match.user2_id == current_user.user_id)
        )
    ).first()
        
        if not existing_match:
            new_match = Match(user1_id=current_user.user_id, user2_id=profile_to_like.user_id)
            existing_like = Like.query.filter_by(liker_id=current_user.user_id, liked_id=profile_to_like.user_id, action='like').first()
            if existing_like:
                existing_like.is_match = 'Yes'
                db.session.commit()
            
            existing_like_rev = Like.query.filter_by(liker_id=profile_to_like.user_id, liked_id=current_user.user_id, action='like').first()
            if existing_like_rev:
                existing_like.is_match = 'Yes'
                db.session.commit()
            
            db.session.add(new_match)
            db.session.commit()
            return jsonify({"message": f"You have matched with {profile_to_like.username}",
                            "match_id": new_match.match_id }), 201

    
    return jsonify({"message": f"You liked {profile_to_like.username}",
                    "likes_count": profile_to_like.likes_received.count()}), 201


@app.route('/api/v1/profiles/<id>/dislike', methods = ['POST'])
@login_required
def dislike_profile(id):
    """
    When users dislike a profile, the dislike is saved to the Likes database.
    """
    profile_to_dislike = User.query.get_or_404(id)
    
    # Check if the user is trying to like themselves
    if current_user.id == profile_to_dislike.id:
        return jsonify({"error": "You cannot dislike your own profile"}), 400

    # Check if user already liked this profile
    if current_user.has_disliked(profile_to_dislike):
        current_user.remove_dislike(profile_to_dislike)
        db.session.commit()
        return jsonify({"message": "Dislike removed"}), 200
    
    current_user.dislike(profile_to_dislike)
    db.session.commit()
    
    return jsonify({"message": f"You disliked {profile_to_dislike.username}"}), 201


@app.route('/api/v1/profiles/<id>/pass', methods=['POST'])
@login_required
def pass_profile(id):
    """
    Check this later
    """
    profile_to_pass = User.query.get_or_404(id)
    
    # Check if interaction already exists
    existing = Like.query.filter_by(liker_id=current_user.user_id, liked_id=profile_to_pass.user_id).first()
    
    if not existing:
        # Save as a 'pass' action so it's filtered out of the algorithm next time
        new_pass = Like(liker_id=current_user.user_id, liked_id=profile_to_pass.user_id, action='pass')
        db.session.add(new_pass)
        db.session.commit()
        return jsonify({"message": "Profile passed. You won't see them again."}), 201
    
    return jsonify({"message": "Already interacted with this profile"}), 200
   

@app.route('/api/v1/contacts/<user_id>', methods=['GET'])
@login_required
def contacts(user_id):
    """
    Displays a contact list of mutual matches.
    """
    contact_ids = Like.query(Like.liked_id).filter_by(user1_id = user_id, is_match="Yes").all()
    contact_list = []
    for contact_id in contact_ids:
        contact = User.query.get_or_404(user_id)
        photo = url_for('get_photo', filename=contact.profile.photo_url) if contact.profile.photo_url else contact.profile.photo_url

        # displays contacts like in whatsapp ig can use either username, 
        # or firstname and lastname in frontend display
        contact_list.append({
            "username": contact.username,
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "photo": photo,
            "bio": contact.profile.bio
        })
    return jsonify({"contacts": contact_list}), 200


@app.route('/api/v1/messages/<match_id>', methods=['GET'])
@login_required
def message_display(match_id):
    """
    Displays messages sent between two users.
    """
    messages = get_message_history(match_id)
    
    message_list = []
    for message in messages:
        message_list.append({
            message_list.append({
                "message_id": message.message_id,
                "sender": message.sender.username,
                "receiver": message.receiver.username,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(), 
})
        })
    return jsonify({"messages": message_list}), 200
    
    
@app.route('/api/v1/messages/<match_id>', methods=['POST'])
@login_required
def send_message(match_id):
    data = request.form
    content = data.get('message')
    match = Match.query.get_or_404(match_id)
    
    if current_user.user_id == match.user1_id:
        receiver_id = match.user2_id
    elif current_user.user_id == match.user2_id:
        receiver_id = match.user1_id
    else:
        return jsonify({"error": "You cannot message this user"}), 403
    new_message = Message(match_id=match_id, sender_id=current_user.user_id, receiver_id=receiver_id, content=content)
    db.session.add(new_message)
    db.session.commit()
    return jsonify({"message": "Message sent!",
                    "message_id": new_message.message_id }), 201

def get_message_history(match_id):
    # return Message.query.filter_by(match_id=match_id).order_by(Message.timestamp.asc()).all()
    match = Match.query.get(match_id)
    if match:
        # gets all messages associated with the match_id shared by the 2 users
        return match.messages.order_by(Message.timestamp.asc()).all()
    return []
        
@app.route('/api/v1/photo/<filename>')
def get_photo(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)  
        
###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404