# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, DateField,FileField
from wtforms.validators import InputRequired, InputRequired, Email, Length, Optional,FileRequired, FileAllowed, SelectMultipleField


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[InputRequired()])

    gender = SelectField('Gender', choices=[
        ('man', 'Man'), 
        ('woman', 'Woman'), 
        ('other', 'Other')
    ])
    
    looking_for = SelectField('Looking For', choices=[
        ('long_term', 'Long-term Relationship'),
        ('casual', 'Casual / Hookups'),
        ('friendship', 'Friendship / Companionship'),
        ('flow', 'Going with the Flow')
    ], validators=[InputRequired()])
    
    password = PasswordField('Password', validators=[
        InputRequired(), 
        Length(min=8)
    ])
    
    submit = SubmitField('Sign Up') 



class EditProfile(FlaskForm):
    # Defining the list within the class or importing it
    PERSONAL_INTERESTS = [
        'Tech', 'Music', 'Art', 'Sports', 'Cooking', 'Travel',
        'Fitness', 'Gaming', 'Reading', 'Film', 
        'Photography', 'Fashion', 'Pets', 'Socializing'
    ]
    
    # Format the list into tuples: ('Tech', 'Tech')
    INTEREST_CHOICES = [(interest, interest) for interest in PERSONAL_INTERESTS]

    visibility = SelectField('Visibility', choices=[('Public', 'Public'), ('Private', 'Private')])
    
    preference = SelectField('Looking for', choices=[('Man', 'Man'), ('Woman', 'Woman'), ('Both', 'Both')])
    
    education = StringField('Education', validators=[Optional(), Length(max=100)])
    
    photo = FileField('Update Profile Photo', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])

    interests = SelectMultipleField('Interests', choices=INTEREST_CHOICES)
    
    bio = TextAreaField('Bio', validators=[Length(max=255)])
    
    location = StringField('Location', validators=[Length(max=100)])
    
    submit = SubmitField('Save Changes')