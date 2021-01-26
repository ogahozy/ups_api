from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired

class TrackForm(FlaskForm):
    num = StringField('Enter your Tracking Number', validators=[DataRequired()])
    submit = SubmitField('Submit')