from datetime import datetime, date
from app import db
from sqlalchemy import text

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # Auto-increments in SQLite, Serial in PG
    username = db.Column(db.String, unique=True, nullable=False)
    hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    events = db.relationship('Event', back_populates='creator', lazy=True)
    joined_events = db.relationship('EventParticipant', back_populates='user', lazy=True, cascade="all, delete-orphan")


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False) # Stored as TEXT (ISO string)
    time = db.Column(db.String)
    description = db.Column(db.String)
    category = db.Column(db.String, default='General')
    capacity = db.Column(db.Integer)
    location = db.Column(db.String)
    location_name = db.Column(db.String)
    image_url = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    creator = db.relationship('User', back_populates='events')
    participants = db.relationship('EventParticipant', back_populates='event', lazy='dynamic', cascade="all, delete-orphan")
    comments = db.relationship('Comment', back_populates='event', lazy=True, cascade="all, delete-orphan")

    @property
    def participants_count(self):
        return self.participants.count()

    @property
    def participant_names(self):
        # Return comma separated list of usernames
        # This acts like GROUP_CONCAT
        return ", ".join([p.user.username for p in self.participants.all()])

    @property
    def creator_username(self):
        return self.creator.username if self.creator else "Unknown"

    def is_joined(self, user_id):
        if not user_id:
            return False
        return self.participants.filter_by(user_id=user_id).first() is not None

    def to_dict(self):
        """Helper to convert to dict if needed for API"""
        return {
            'id': self.id,
            'title': self.title,
            'date': self.date,
            'description': self.description,
            'category': self.category,
            'image_url': self.image_url
        }


class EventParticipant(db.Model):
    __tablename__ = 'event_participants'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    joined_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    user = db.relationship('User', back_populates='joined_events')
    event = db.relationship('Event', back_populates='participants')


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    user = db.relationship('User', back_populates='comments')
    event = db.relationship('Event', back_populates='comments')

# Update User relationship for comments (can be done by adding property here to User or simpler, just backref)
User.comments = db.relationship('Comment', back_populates='user', lazy=True)
