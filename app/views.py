"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file
from datetime import date, datetime  
from app.models import db, User, Profile
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


@app.route('/api/search', methods=['GET'])
#@login_required
def search_profiles():
    # Query parameters - will revise for preferences: sexuality, age range, location, education, religion
    first_name = request.args.get('first_name', '').strip()
    location = request.args.get('location', '').strip()
    min_age = request.args.get('min_age', type=int)
    max_age = request.args.get('max_age', type=int)
    interests = request.args.getlist('looking_for')
    gender = request.args.get('gender', '').strip()
    
    if not any([first_name, location, min_age, max_age, interests, gender]):
        return jsonify(error="At least one search parameter is required"), 400
    
    query = db.session.query(Profile, User).join(User, Profile.user_id_fk == User.user_id)
    
    # Apply filters based on provided parameters - gender, education, religion 
    #Preferences: sexuality, age range, location, education, religion
    if first_name:
        query = query.filter(User.first_name.ilike(f'%{first_name}%'))
    if location:
        query = query.filter(Profile.location.ilike(f'%{location}%'))
    if min_age is not None:
        query = query.filter(Profile.age >= min_age)
    if max_age is not None:
        query = query.filter(Profile.age <= max_age)
    if interests:
        query = query.filter(Profile.interests.in_(interests))
    if gender:
        query = query.filter(Profile.gender.ilike(f'%{gender}%'))
    results = query.all()

    # Sort options (newest, most similar, etc.)
    sort_by = request.args.get('sort_by', 'newest')
    if sort_by == 'newest':
        results.sort(key=lambda x: x[0].created_at, reverse=True)
    elif sort_by == 'most_similar':
        current_user_profile = Profile.query.filter_by(user_id=request.user_id).first()  # Implement this function to get the current user's profile
        # Implementation of matching algorithm to calculate similarity score between profiles
        #results.sort(key=lambda x: get_match_score(current_user_profile, x[0]), reverse=True)
    
    # Format results for JSON response
    formatted_results = []
    for profile, user in results:
        age = (
            (datetime.today - user.dob).days // 365 
            if user.dob else None
        )
        formatted_results.append({
            #Results should include profile information and user information
        })
    
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