"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os
from app import app
from . import db 
from . import login_manager

from app.models import User, Profile, Preference, Like, Match, Message, SavedProfile, Notification
from flask_socketio import emit
from .forms import LoginForm, SignUpForm, EditProfile, MessageForm, PreferencesForm
from flask import render_template, request, jsonify, send_file, flash, send_from_directory, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_
from datetime import date, datetime

print("!!! SERVER IS STARTING !!!", flush=True)


###
# Routing for your application.
###


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):

    root_dir = os.path.abspath(os.path.dirname(__file__))
    project_dir = os.path.abspath(os.path.join(root_dir, '..'))

    file_path = os.path.join(project_dir, path)

    if path != "" and os.path.exists(file_path):
        return send_from_directory(project_dir, path)

    return send_from_directory(project_dir, 'index.html')

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

###
# User Authentification and Profile Management 
###
@app.route('/api/v1/auth/login', methods=['POST'])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    #Here for Debugging purposes 
    print("DATA:", data)
    print("EMAIL:", email)
    print("PASSWORD:", password)

    print(generate_password_hash("Password123!", method='pbkdf2:sha256'))
    

    

    if not email or not password:
        return jsonify({"error": "Missing credentials"}), 400

    user = User.query.filter_by(email=email).first()
    print("USER:", user)

    print("HASH IN DB:", user.password_hash)
    print("PASSWORD CHECK:", check_password_hash(user.password_hash, password))

    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({
            "message": "Login successful",
            "user": {
                "username": user.username,
                "user_id": user.user_id
            }
        }), 200

    return jsonify({"error": "Invalid email or password"}), 401


import traceback # Add this at the top of your file

@app.route('/api/v1/signup', methods=['POST'])
def signup():
    data = request.get_json()
    required_fields = ["first_name", "last_name", "username", "email", "password", "gender"]

    # 1. Validation checks
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400
    
    dob_raw = data.get("dob")
    dob_object = None
    if dob_raw:
        try:
            dob_object = datetime.strptime(dob_raw, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400

    try:
        # 1. Create the User object
        new_user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            username=data["username"],
            email=data["email"],
            gender=data["gender"],
            dob=dob_object,
            password=data["password"]
        )
        db.session.add(new_user)
        
        # Use flush to get the new_user.user_id without committing yet
        db.session.flush() 

        # 2. Create the Profile object linked to that ID
        new_profile = Profile(
            user_id=new_user.user_id,
            visibility="Public"
        )
        db.session.add(new_profile)

        # 3. Commit EVERYTHING at once
        db.session.commit()
        print(f"✅ SUCCESS: User {new_user.username} and Profile saved.")
        
        return jsonify({"message": f"Welcome {new_user.username}!"}), 201

    except Exception as e:
        db.session.rollback()
        print("❌ DATABASE ERROR:")
        traceback.print_exc() # This will show the EXACT error in your terminal
        return jsonify({"error": "Registration failed", "details": str(e)}), 500
# @app.route('/api/v1/signup', methods=['POST'])
# def signup():
#     data = request.get_json() 
    
#     #Instantiate SignUpForm with JSON data
#     form = SignUpForm(data=data)

#     #Validates the form
#     if form.validate():
#         # Check if email already exists
#         if User.query.filter_by(email=form.email.data).first():
#             return jsonify({"error": "Email already exists"}), 400

#         try:
#             # Creates the User object using form data
#             new_user = User(
#                 first_name=form.first_name.data,
#                 last_name=form.last_name.data,
#                 username=form.username.data,
#                 dob=form.dob.data,
#                 looking_for=form.looking_for.data or 'Casual',
#                 password_hash=generate_password_hash(form.password.data),
#                 email=form.email.data,
#                 gender=form.gender.data
#             )
            
#             db.session.add(new_user)
#             db.session.flush() # Generates user_id

#             # Creates the Profile object automatically
#             new_profile = Profile(
#                 user_id=new_user.user_id, 
#                 visibility="Public", #Sets visibility of Profile to public automatically 
#                 education=None,
#                 photo_url=None,
#                 bio=None,
#                 location=None
#             )
            
#             db.session.add(new_profile)
#             db.session.commit() 

#             return jsonify({"message": f"Welcome to DriftDater {new_user.username}!"}), 201
            
#         except Exception as e:
#             db.session.rollback() 
#             return jsonify({"error": "An error occurred during registration."}), 500

#     #Returns validation errors (e.g., "Field Required" or "Invalid Email")
#     return jsonify({"errors": form.errors}), 400
    

    
@app.route('/api/v1/auth/logout', methods=['POST'])
@login_required
def logout():
    """
    Clears the session cookie and logs the user out
    """
    logout_user()
    
    return jsonify({
        "status": "success",
        "message": "See you later! Hope your next match is just a 'drift' away."
    }), 200



@app.route('/api/v1/profile/all', methods=['GET'])
@login_required 
def list_profile():
    """
    Lists all user Profiles
    """

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

 
@app.route('/api/v1/profile/<int:user_id>', methods=['GET'])
@login_required 
def single_profile(user_id):
    """
    Gets a singular Profile when clicked on 
    """

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


@app.route('/api/v1/profile', methods=['GET'])
@login_required 
def display_profile():
    """
    Displays current user's profile
    """
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


@app.route('/api/v1/profile/edit', methods=['PUT'])
@login_required
def edit_profile():

    data = request.get_json()
    photo = request.files.get('photo')

    # Instantiate form (same as signup style)
    form = EditProfileForm(data=data, csrf_enabled=False)

    # Validate form
    if form.validate():

        profile = Profile.query.filter_by(user_id=current_user.user_id).first()

        if not profile:
            return jsonify({"error": "Profile not found"}), 404

        try:

            # Handle photo upload separately (not part of JSON)
            if photo:
                filename = secure_filename(photo.filename)
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                photo.save(upload_path)
                profile.photo_url = filename

            # Update profile fields
            profile.update_profile(
                visibility=form.visibility.data,
                education=form.education.data,
                bio=form.bio.data,
                location=form.location.data
            )

            db.session.commit()

            return jsonify({
                "message": "Profile updated successfully",
                "photo_url": profile.photo_url
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({
                "error": "An error occurred while updating profile."
            }), 500

    # Return validation errors (same style as signup)
    return jsonify({"errors": form.errors}), 400



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
        

@app.route('/api/v1/profiles/set-preferences', methods=['POST'])
@login_required
def set_preferences():

    data = request.get_json()

    # Instantiate form with JSON (same as signup)
    form = PreferencesForm(data=data, csrf_enabled=False)

    # Validate form
    if form.validate():
        try:
            # Get existing preference OR create new one
            preference = Preference.query.filter_by(user_id=current_user.user_id).first()

            if not preference:
                preference = Preference(user_id=current_user.user_id)
                db.session.add(preference)

            preference.gender_pref = form.gender_pref.data
            preference.education_pref = form.education_pref.data
            preference.religion_pref = form.religion_pref.data
            preference.age_min = form.age_min.data or 18
            preference.age_max = form.age_max.data or 99

            db.session.commit()

            return jsonify({
                "message": "Preferences updated successfully",
                "preferences": {
                    "gender_pref": preference.gender_pref,
                    "education_pref": preference.education_pref,
                    "religion_pref": preference.religion_pref,
                    "age_min": preference.age_min,
                    "age_max": preference.age_max
                }
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "An error occurred while saving preferences."}), 500

    # Validation errors (same style as signup)
    return jsonify({"errors": form.errors}), 400


###
# Matching Algorithm
###

def calculate_match_score(user, profile): #user is a dict put together in another function
    """
    Calculates a match score based on 4 categories.
    Categories: Location, Age, Interests and Gender
    """
    score = 0
    candidate = {'location': profile.location, 'age': profile.age(), 'interests': profile.interests, 'gender': profile.user.gender}
    user_pref = {'location': user.profile.location, 'age': [user.preferences.age_min, user.preferences.age_max], 'interests': user.profile.interests, 'gender': user.preferences.gender_pref}
        
    # Weights for each category (optional, adds precision)
    weights = {'location': 0.5, 'age': 1.5, 'interests': 0.5, 'gender': 1.5} 
        
    if candidate['location'] == user_pref['location']:
        score += weights['location']
        
    min_age = user_pref['age'][0]
    max_age = user_pref['age'][1]
    if candidate['age'] >= min_age and candidate['age'] <= max_age: 
        score += weights['age'] 

    #Adds 0.5 to score for each matching interest.
    for i in candidate['interests']:
        if i in user_pref['interests']: 
            score += weights['interests']
            
    if candidate['gender'] == user_pref['gender'] or user_pref['gender'] == 'Both':
        score += weights['gender']
        
    return score

@app.route('/api/v1/matches', methods = ['GET'])
@login_required
def display_matches(): 
    """
    Displays matched profiles to logged in users
    """
    user_id = current_user.user_id
    
    #remove all profiles the user has already viewed
    interacted = db.session.query(Like.liked_id).filter(Like.liker_id == user_id).all()
    interacted_ids = [i[0] for i in interacted] + [user_id]
    
    profiles = db.session.execute(db.select(Profile)).filter(~Profile.user_id.in_(interacted_ids)).scalars()
    
    user = db.session.execute(db.select(User).filter_by(user_id=user_id)).scalar_one() 
    
    scored_match_list = []
    for profile in profiles:
        score = calculate_match_score(user, profile)
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
    if current_user.user_id == profile_to_like.id:
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
    like_notification = Notification(user_id=profile_to_like.user_id, 
                                     message=f"{current_user.profile.username} liked your profile!")
    db.session.add(like_notification)
    emit('new_notification', {'message': f"{current_user.profile.username} liked your profile!"}, 
         room=str(profile_to_like.user_id), namespace='/')
    
    is_mutual = profile_to_like.has_liked(current_user)
    

    if is_mutual:
        existing_match = Match.query.filter(
        or_(
            (Match.user1_id == current_user.user_id) & (Match.user2_id == profile_to_like.user_id),
            (Match.user1_id == profile_to_like.user_id) & (Match.user2_id == current_user.user_id)
        )
    ).first()
        
        if not existing_match:
            new_match = Match(user1_id=current_user.user_id, user2_id=profile_to_like.user_id)
            db.session.add(new_match)
            
            existing_like = Like.query.filter_by(liker_id=current_user.user_id, liked_id=profile_to_like.user_id, action='like').first()
            if existing_like:
                existing_like.is_match = 'Yes'

            existing_like_rev = Like.query.filter_by(liker_id=profile_to_like.user_id, liked_id=current_user.user_id, action='like').first()
            if existing_like_rev:
                existing_like_rev.is_match = 'Yes'

            # Notification to current user
            match_notification_1 = Notification(user_id=current_user.user_id, 
                                     message=f"You have matched with {profile_to_like.profile.username}!")
            # Notification to liked_user
            match_notification_2 = Notification(user_id=profile_to_like.user_id, 
                                     message=f"You have matched with {current_user.profile.username}!")
            
            db.session.add_all([match_notification_1, match_notification_2])
            
            
            # Notification to current user
            emit('new_match', {'message': f"Match! You and {profile_to_like.profile.username} liked each other!"}, 
                 room=str(current_user.user_id), namespace='/')
            
            # Notification to liked_user
            emit('new_match', {'message': f"Match! You and {current_user.profile.username} liked each other!"}, 
                 room=str(profile_to_like.user_id), namespace='/')

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
    if current_user.user_id == profile_to_dislike.user_id:
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
    
    new_notif = Notification(user_id=receiver_id, 
                            message=f"{current_user.profile.username} sent you a message.")
    db.session.add(new_notif)
    
    emit('new_message', {'message': f"{current_user.profile.username} sent you a message."}, 
                 room=str(receiver_id), namespace='/')
    
    db.session.commit()
    return jsonify({"message": "Message sent!",
                    "message_id": new_message.message_id }), 201

@app.route('/api/v1/notifications', methods=['GET'])
@login_required
def display_notifications():
    """
    Retrieves all notifications for the current user.
    """
    notifications = Notification.query.filter_by(user_id=current_user.user_id) \
                                      .order_by(desc(Notification.timestamp)) \
                                      .all()
    notification_list = []
    for notif in notifications:
        notification_list.append({
            'id': notif.id,
            'message': notif.message,
            'timestamp': notif.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
          
    return jsonify({"notifications": notification_list}), 200
    

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
        

@app.route('/api/search', methods=['GET'])
@login_required
def search_profiles():
    # Query parameters for searching profiles
    first_name = request.args.get('first_name', '').strip()
    last_name = request.args.get('last_name', '').strip()
    min_age = request.args.get('min_age', type=int)
    max_age = request.args.get('max_age', type=int)
    preference = request.args.get('preference', '').strip()
    location = request.args.get('location', '').strip()
    education = request.args.get('education', '').strip()
    #religion = request.args.get('religion', '').strip()
    interests = request.args.get('interests', '').strip()
    
    if not any([first_name, last_name,location, min_age, max_age, preference, education, interests ]): #religion, ]):
        return jsonify(error="At least one search parameter is required"), 400
    
    query = db.session.query(Profile, User).join(User, Profile.user_id_fk == User.user_id)
    
    # Apply filters based on parameters: preference(sexuality), age range, location, education, religion
    if first_name:
        query = query.filter(User.first_name.ilike(f'%{first_name}%'))
    if preference:
        query = query.filter(Profile.preference.ilike(f'%{preference}%'))
    if location:
        query = query.filter(Profile.location.ilike(f'%{location}%'))
    if education:
        query = query.filter(Profile.education.ilike(f'%{education}%'))
    if interests:
        query = query.filter(Profile.interests.ilike(f'%{interests}%'))
    #if religion:
        #query = query.filter(Profile.religion.ilike(f'%{religion}%'))
        
    today = date.today()
    
    if min_age is not None:
        max_birthdate = date(today.year - min_age, today.month, today.day)
        query = query.filter(User.dob <= max_birthdate)
    if max_age is not None:
        min_birthdate = date(today.year - max_age, today.month, today.day)
        query = query.filter(User.dob >= min_birthdate)
    results = query.all()

    # Sort options (newest, most similar, etc.)
    sort_by = request.args.get('sort_by', 'newest')
    if sort_by == 'newest':
        #query = query.order_by(Profile.created_at.desc())
        results.sort(key=lambda x: x[0].created_at, reverse=True)
    elif sort_by == 'most_similar':
        current_user_profile = User.query.filter_by(user_id=current_user.user_id).first() 
        results.sort(key=lambda x: calculate_match_score(current_user_profile, x[0]), reverse=True)
    
    # Format results for JSON response
    formatted_results = []
    for profile, user in results:
        formatted_results.append({
            'user_id': user.user_id,
            'username': user.username,
            'first_name': user.first_name,
            'age': age_range(profile.age),
            'bio': profile.bio,
            'photo': profile.photo_url,
            'location': profile.location,
            'gender': profile.gender,
            'looking_for': profile.looking_for,
            'interests': profile.interests,
            'preference': profile.preference,
            'education': profile.education,
            #'religion': profile.religion,
        })
    return jsonify(profiles=formatted_results), 200



# @app.route('/api/v1/bookmarks', methods=['POST'])
# #@login_required
# def bookmark_profiles():
#     profile_id = request.json.get('profile_id')
    
#     if not profile_id:
#         return jsonify(error="Profile ID is required"), 400
    
#     profile = Profile.query.get(profile_id)
#     if not profile:
#         return jsonify(error="Profile not found"), 404
    
#     existing_bookmark = Like.query.filter_by(liker_id=request.user_id, liked_id=profile_id, action='bookmark').first()
#     if existing_bookmark:
#         return jsonify(error="Profile already bookmarked"), 400
    
#     # Use of Like table with action='bookmark' inlcuded with 'like/dislike OR can use a separate Bookmark table
#     bookmark = Like.query.filter_by(liker_id=request.user_id, action='bookmark')
#     db.session.add(bookmark)
#     db.session.commit()
    
#     return jsonify(message="Profile bookmarked successfully"), 200
        

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