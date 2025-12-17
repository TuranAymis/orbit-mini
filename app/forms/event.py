from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, SelectField, IntegerField, SubmitField, URLField
from wtforms.validators import DataRequired, Optional, URL, NumberRange, Length, Regexp, ValidationError
from datetime import date, timedelta

def validate_future_date(form, field):
    if field.data < date.today():
        raise ValidationError("Date cannot be in the past.")
    if field.data > date.today() + timedelta(days=730): # 2 Years
        raise ValidationError("Date cannot be more than 2 years in the future.")

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    date = DateField('Date', validators=[DataRequired(), validate_future_date])
    time = TimeField('Time', validators=[Optional()])
    category = SelectField('Category', choices=[
        ('General', 'General'),
        ('Tech', 'Tech'),
        ('Social', 'Social'),
        ('Sports', 'Sports'),
        ('Art', 'Art'),
        ('Education', 'Education'),
        ('Music', 'Music'),
        ('Food', 'Food & Drink'),
        ('Other', 'Other')
    ])
    description = TextAreaField('Description', validators=[Length(max=500)])
    capacity = IntegerField('Capacity', validators=[Optional(), NumberRange(min=1, message="Capacity must be at least 1")])
    location_name = StringField('Location Name', validators=[Length(max=100)])
    location = URLField('Google Maps Link', validators=[
        Optional(), 
        URL(message="Invalid URL"), 
        Regexp(r'^https://(www\.)?google\.com/maps.*', message="Must be a valid Google Maps URL")
    ])
    image_url = URLField('Image URL', validators=[Optional(), URL(message="Invalid URL"), Length(max=500)])
    submit = SubmitField('Save Event')

class CommentForm(FlaskForm):
    content = TextAreaField('Join the discussion...', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Post Comment')
