"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file, flash
from flask_login import login_user, logout_user, verify_password, login_required, current_user
from .forms import LoginForm, SignUpForm, EditProfile
from .models import User, Profile 
from . import db 
from werkzeug.utils import secure_filename
import os


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/login', methods=['POST']) 
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


@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json() 
    
    #Checks to see if email is already registered  
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({"error": "Email already exists"}), 400

    try:
        new_user = User(
            email=data.get('email'),
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            # Ensure data.get('dob') is converted to a date object if necessary
            dob=data.get('dob'), 
            gender=data.get('gender')
        )
        new_user.set_password(data.get('password'))
        
        db.session.add(new_user)
        db.session.flush() 

        new_profile = Profile(
            user_id=new_user.id,
            preference=data.get('looking_for'), #Should we do this 
            visibility="Public", #Sets Visibility as Default 
            education=None,
            photo_url=None,
            bio=None,
            location=None
        )
        
        db.session.add(new_profile)
        db.session.commit() 

        #We could do a message that says "Welcome to DriftDater [USER] !"
        return jsonify({"message": "User and Profile created successfully!"}), 201
        
    except Exception as e:
        db.session.rollback() 
        return jsonify({"error": str(e)}), 500
    

#MAY NOT BE NEEDED 
# @app.route('/api/profile/create', methods=['POST'])
# #@login_required 
# def create_profile():
#     data = request.get_json()
    
#     new_profile = Profile(
#         user_id=data.get('user_id'),
#         age=data.get('age'),
#         photo=data.get('photo_url'),
#         bio=data.get('bio'),
#         location=data.get('location')
#     )
    
#     db.session.add(new_profile)

#     db.session.commit()
    
#     return jsonify({"message": "Profile saved!"}), 201

@app.route('/api/profile', methods=['GET'])
#@login_required 
def display_profile():
    data = request.get_json()
    
    profile = Profile.query.filter_by(username=current_user).first()

    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    current_age = profile.age 
    age_display = age_range(current_age)

    return jsonify({
        "username": profile.user.username, 
        "first_name": profile.user.first_name,
        "age": age_display,
        "bio": profile.bio,
        "photo": profile.photo_url,
        "location": profile.location,
        "gender": profile.gender,
        "looking_for": profile.looking_for,
        "interests": profile.interests
    }), 200


@app.route('/api/profile/edit', methods=['PUT'])
# @login_required
def edit_profile():

    profile = Profile.query.filter_by(user_id=current_user.user_id).first()
    data = request.form
    photo = request.files.get('photo')

    try:
        
        if data.get('bio') and len(data.get('bio')) > 255:
            return jsonify({"error": "Bio too long"}), 400

        
        if photo:
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.root_path, 'app/uploads', filename))
            profile.photo_url = filename

        
        profile.update_profile(
            visibility=data.get('visibility'),
            preference=data.get('preference'),
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
        

@app.route('/api/logout')
#@login_required
def logout():
    logout_user()
    #return redirect()
    pass


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