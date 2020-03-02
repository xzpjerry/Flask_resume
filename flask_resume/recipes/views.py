from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SelectField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

import pycountry

from flask_resume import AVATARS

DEFAULT_COUNTRIES = [(None, '')] + [(country.alpha_2, country.name) for country in sorted(pycountry.countries, key=lambda x: x.name)]
class BasicResumeEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    nation = SelectField('Nation', validators=[DataRequired()], choices=DEFAULT_COUNTRIES)
    region = SelectField('Region',validators=[DataRequired()], choices=[(None, '')])
    birth = DateField('Birthdate', format='%Y-%m-%d', validators=[DataRequired()])
    portrait = FileField('Upload Your Avatar', validators=[FileAllowed(AVATARS, 'Image only!'), ])
    submit = SubmitField("Save")