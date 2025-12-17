from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, SelectField, IntegerField, SubmitField, URLField
from wtforms.validators import DataRequired, Optional, URL, NumberRange

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
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
    description = TextAreaField('Description')
    capacity = IntegerField('Capacity', validators=[Optional(), NumberRange(min=1, message="Capacity must be at least 1")])
    location_name = StringField('Location Name')
    location = URLField('Google Maps Link', validators=[Optional(), URL(message="Invalid URL")])
    image_url = URLField('Image URL', validators=[Optional(), URL(message="Invalid URL")])
    submit = SubmitField('Save Event')

class CommentForm(FlaskForm):
    content = TextAreaField('Join the discussion...', validators=[DataRequired()])
    submit = SubmitField('Post Comment')
