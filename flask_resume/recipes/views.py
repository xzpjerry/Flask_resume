from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SelectField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

import pycountry

from flask_resume import AVATARS

class CountrySelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountrySelectField, self).__init__(*args, **kwargs)
        self.choices = [(country.alpha_2, country.name) for country in pycountry.countries]

class BasicResumeEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    nation = CountrySelectField('Nation', validators=[DataRequired()])
    region = StringField('Region', validators=[DataRequired()])
    birth = DateField('Birthdate', format='%Y-%m-%d', validators=[DataRequired()])
    portrait = FileField('Upload Your Avatar', validators=[FileAllowed(AVATARS, 'Image only!'), FileRequired('File was empty!')])
    submit = SubmitField("Save")