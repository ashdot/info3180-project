# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, DateField
from wtforms.validators import InputRequired, InputRequired, Email, Length


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
