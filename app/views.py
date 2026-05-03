"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file
from datetime import date, datetime  
from app.models import db, User, Profile, Preference, Like
import os


###
# Routing for your application.
###


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """Serve static files."""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_file(os.path.join(app.static_folder, path))
    else:
        return render_template('home.html')

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/v1/search', methods=['GET'])
#@login_required
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
        results.sort(key=lambda x: x[0].created_at, reverse=True)
    elif sort_by == 'most_similar':
        current_user_profile = Profile.query.filter_by(user_id=request.user_id).first() 
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

@app.route('/api/v1/bookmarks', methods=['POST'])
#@login_required
def bookmark_profiles():
    profile_id = request.json.get('profile_id')
    
    if not profile_id:
        return jsonify(error="Profile ID is required"), 400
    
    profile = Profile.query.get(profile_id)
    if not profile:
        return jsonify(error="Profile not found"), 404
    
    existing_bookmark = Like.query.filter_by(liker_id=request.user_id, liked_id=profile_id, action='bookmark').first()
    if existing_bookmark:
        return jsonify(error="Profile already bookmarked"), 400
    
    # Use of Like table with action='bookmark' inlcuded with 'like/dislike OR can use a separate Bookmark table
    bookmark = Like.query.filter_by(liker_id=request.user_id, action='bookmark')
    db.session.add(bookmark)
    db.session.commit()
    
    return jsonify(message="Profile bookmarked successfully"), 200
    
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