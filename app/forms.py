# Add any form classes for Flask-WTF here

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, DateField,FileField
from wtforms.validators import InputRequired, InputRequired, Email, Length, Optional,FileRequired, FileAllowed

class MessageForm(FlaskForm):
    message = TextAreaField("Message")
    submit = SubmitField('Send') 