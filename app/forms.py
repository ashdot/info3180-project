# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
<<<<<<< HEAD
from wtforms import StringField, IntegerField, PasswordField, TextAreaField, SelectField, SubmitField, DateField,FileField
#from wtforms.validators import InputRequired, InputRequired, Email, Length, Optional,FileRequired, FileAllowed, SelectMultipleField,NumberRange, Optional
# 1. Standard WTForms validators
from wtforms.validators import InputRequired, Email, Length, Optional, NumberRange
=======
from wtforms import StringField, IntegerField, PasswordField, TextAreaField, SelectField, SubmitField, DateField,FileField, SelectMultipleField
#from wtforms.validators import InputRequired, InputRequired, Email, Length, Optional,FileRequired, FileAllowed, SelectMultipleField,NumberRange, Optional
from wtforms.validators import InputRequired, Email, Length, Optional, NumberRange
from flask_wtf.file import FileRequired, FileAllowed
>>>>>>> bdc24b5 (Added favourites page)

# 2. Flask-WTF specific file validators (This is what was missing)
from flask_wtf.file import FileRequired, FileAllowed

# 3. Fields come from wtforms directly
from wtforms import SelectMultipleField

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


class MessageForm(FlaskForm):
    message = StringField('Message', validators=[InputRequired()])
    submit = SubmitField('Send')


class PreferencesForm(FlaskForm):

    # Gender Preference
    gender_pref = SelectField(
        'Gender Preference',
        choices=[
            ('Everyone', 'Everyone'),
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Non-binary', 'Non-binary')
        ],
        validators=[Optional()]
    )

    # Education Level Preference
    education_pref = SelectField(
        'Education Level',
        choices=[
            ('Any', 'Any'),
            ('High School', 'High School'),
            ('Bachelors', 'Bachelors'),
            ('Masters', 'Masters'),
            ('PhD', 'PhD')
        ],
        validators=[Optional()]
    )

    # Religion Preference
    religion_pref = SelectField(
        'Religion Preference',
        choices=[
            ('Open', 'Open'),
            ('Christian', 'Christian'),
            ('Muslim', 'Muslim'),
            ('Atheist', 'Atheist'),
            ('Other', 'Other')
        ],
        validators=[Optional()]
    )

    # Age Range 
    age_min = IntegerField(
        'Minimum Age',
        default=18,
        validators=[NumberRange(min=18, max=99)]
    )
    
    age_max = IntegerField(
        'Maximum Age',
        default=99,
        validators=[NumberRange(min=18, max=99)]
    )

    submit = SubmitField('Save Preferences')

# Custom validator to ensure min isn't higher than max - GEMINI 
def validate(self, extra_validators=None):
    initial_validation = super(PreferencesForm, self).validate(extra_validators)
    if not initial_validation:
        return False
    
    if self.age_min.data > self.age_max.data:
        self.age_min.errors.append('Minimum age cannot be greater than maximum age.')
        return False
    return True