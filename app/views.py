"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os
from app import app, db
from app.models import User, Like, Match
from flask import render_template, request, jsonify, send_file
from flask_login import login_user, logout_user, current_user, login_required



###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


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
        
    if candidate['location'] in user['location']:
        score += weights['location']
        
    min_age = user['age'][:2]
    max_age = user['age'][-2:]
    if candidate['age'] >= min_age and candidate['age'] <= max_age: 
        score += weights['age'] 

    #Adds 0.5 to score for each matching interest.
    for i in candidate['interests']:
        if i in user['interests']: #maybe use the lower function on all items in user interests with a loop
            score += weights['interests']
            
    if candidate['gender'] == user['gender']:
        score += weights['gender']
    return score

@app.route('/api/v1/matches', methods = ['GET'])
@login_required
def display_matches(): 
    """
    Displays matched profiles to logged in users
    """
    user_id = current_user.id
    # whatever the profile database is called
    profiles = db.session.execute(db.select(UserProfile)).scalars() 
    # maybe looking_for in user should be a different table for preferences
    user = db.session.execute(db.select(UserPreference).filter_by(user_id=user_id)).scalar_one() 
    best_match = []
    okay_match = []
    unlikely_match = []
    for profile in profiles:
        candidate = {'location': profile.location, 'age': profile.age, 'interests': profile.interests, 'gender': profile.gender}
        score = calculate_match_score(user, candidate)
        if score >= 4:
            best_match.append([profile, score])
        elif 2 <= score <= 4:
            okay_match.append([profile, score])
        else:
            unlikely_match.append([profile, score])
    match_list = []
    for match in best_match:
        match_list.append({
            "id": match[0].user_id,
            "location": match[0].location,
            "age": match[0].age,
            "interests": match[0].interests,
            "gender": match[0].gender,
            "score": match[1]
        })
    # We can either make another for loop for okay matches
    # or we can combine the good and okay matches 
    # and not track the unlikely matches

    return jsonify({"matches": match_list}), 200
    #frontend team will display matches within this list
    
@app.route('/api/v1/profiles/<:id>/like', methods = ['POST'])
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

    # Check if user already liked this profile
    if current_user.has_liked(profile_to_like):
        return jsonify({"message": "You already liked this profile"}), 200
    
    current_user.like(profile_to_like)
    db.session.commit()
    total_likes = profile_to_like.likes_received.count()
    
    is_mutual = profile_to_like.has_liked(current_user)
    
    if is_mutual:
        # We don't create the Match record yet! 
        # We tell the frontend to ask the user for confirmation.
        return jsonify({
            "message": "Potential Match!",
            "is_mutual": True,
            "profile_id": id,
            "username": profile_to_like.username
        }), 200
    
    return jsonify({"message": f"You liked {profile_to_like.username}",
                    "likes_count": profile_to_like.likes_received.count()}), 201



@app.route('/api/v1/profiles/<int:id>/confirm-match', methods=['POST'])
@login_required
def confirm_match(id):
    """
    If the user confirms the match, it is saved to the match database.
    """
    profile = User.query.get_or_404(id)

    # Verify both users actually like each other before creating the record
    if current_user.has_liked(profile) and profile.has_liked(current_user):
        
        # Check if match already exists to prevent duplicates
        existing_match = Match.query.filter(
            ((Match.user1_id == current_user.user_id) & (Match.user2_id == profile.user_id)) |
            ((Match.user1_id == profile.user_id) & (Match.user2_id == current_user.user_id))
        ).first()

        if not existing_match:
            new_match = Match(user1_id=current_user.user_id, user2_id=profile.user_id)
            db.session.add(new_match)
            db.session.commit()
            return jsonify({"message": "Match confirmed and saved!"}), 201
        
        return jsonify({"message": "Match already exists"}), 200

    return jsonify({"error": "Mutual like not found"}), 400

    
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