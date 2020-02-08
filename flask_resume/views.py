from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SelectField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

import pycountry

from gbconfig import AVATARS

class CountrySelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountrySelectField, self).__init__(*args, **kwargs)
        self.choices = [(country.alpha_2, country.name) for country in pycountry.countries]

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)
    submit = SubmitField("Send")

class SignupForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Send")

class BasicResumeEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    nation = CountrySelectField('Nation', validators=[DataRequired()])
    region = StringField('Region', validators=[DataRequired()])
    birth = DateField('Birthdate', format='%Y-%m-%d', validators=[DataRequired()])
    portrait = FileField('Upload Your Avatar', validators=[FileAllowed(AVATARS, 'Image only!'), FileRequired('File was empty!')])
    submit = SubmitField("Savw")