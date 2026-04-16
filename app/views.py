"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file, flash
from flask_login import login_user, logout_user, verify_password, login_required 
from .forms import LoginForm, SignUpForm
from .models import User, Profile 
from . import db 
import os


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


# @app.route('/api/login', methods=['GET','POST'])
# def login():
#     if request.method == 'POST':

#         email = request.form['email']
#         password = request.form['password']
#         user_data = User.query.filter_by(email=email).first()

#         if user_data and verify_password(password, user_data.password):

#             
#              
            
#             
#             
#             

#     #Connect to Vue 
#     pass


@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json() 
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({"error": "Email already exists"}), 400

    try:
        new_user = User(
            email=data.get('email'),
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            dob=data.get('dob'), 
            gender=data.get('gender'),
            looking_for=data.get('looking_for')
        )
        new_user.set_password(data.get('password'))
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"message": "User created successfully!"}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/profile/create', methods=['POST'])
#@login_required 
def create_profile():
    data = request.get_json()
    
    
    new_profile = Profile(
        user_id=data.get('user_id'),
        age=data.get('age'),
        photo=data.get('photo_url'),
        bio=data.get('bio'),
        location=data.get('location')
    )
    
    db.session.add(new_profile)

    db.session.commit()
    
    return jsonify({"message": "Profile saved!"}), 201

@app.route('/api/profile', methods=['GET'])
#@login_required 
def display_profile():
    data = request.get_json()
    
    
    profile = Profile.query.filter_by(username=current_user).first()
    
    return jsonify({
        "username": profile.user.username, # Accessing via backref
        "first_name": profile.user.first_name,
        "age": profile.age,
        "bio": profile.bio,
        "photo": profile.photo,
        "location": profile.location,
        "gender": profile.gender,
        "looking_for": profile.looking_for
    }), 200

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