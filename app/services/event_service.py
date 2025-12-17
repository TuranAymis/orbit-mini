from datetime import date
from sqlalchemy import func, case, text
from app import db
from app.models.models import Event, EventParticipant, User

class EventService:
    @staticmethod
    def create_event(user_id, event_data):
        """Creates a new event with spam check"""
        # Spam Protection: Check for duplicates
        existing_event = Event.query.filter_by(
            user_id=user_id,
            title=event_data['title'],
            date=event_data['date']
        ).first()
        
        if existing_event:
            return None, "Event already exists"

        # Handle capacity
        capacity = event_data.get('capacity')
        if not capacity:
            capacity = None
        else:
            capacity = int(capacity)

        new_event = Event(
            user_id=user_id,
            title=event_data['title'],
            date=event_data['date'],
            time=event_data.get('time'),
            category=event_data.get('category', 'General'),
            description=event_data.get('description'),
            capacity=capacity,
            location=event_data.get('location'),
            location_name=event_data.get('location_name'),
            image_url=event_data.get('image_url')
        )
        
        db.session.add(new_event)
        db.session.commit()
        return new_event, "Event created successfully"

    @staticmethod
    def add_comment(user_id, event_id, content):
        """Adds a comment to an event"""
        from app.models.models import Comment
        if not content:
            return False, "Content cannot be empty"

        new_comment = Comment(
            user_id=user_id,
            event_id=event_id,
            content=content
        )
        db.session.add(new_comment)
        db.session.commit()
        return new_comment, "Comment added successfully"

    @staticmethod
    def get_comments(event_id):
        """Get comments for an event"""
        from app.models.models import Comment
        return Comment.query.filter_by(event_id=event_id).order_by(Comment.created_at.desc()).all()

    @staticmethod
    def get_event_with_details(event_id, current_user_id=None):
        """Returns event with participant count and join status"""
        # Since we use ORM, some of this is easier handled in the loop or with hybrid properties,
        # but to keep efficient bulk loading patterns similar to previous raw SQL:
        return db.session.get(Event, event_id)

    @staticmethod
    def get_upcoming_events(user_id, search_query='', category_filter=''):
        """Fetch upcoming events with filters"""
        today = str(date.today())
        
        query = Event.query.filter(Event.date >= today)
        
        if search_query:
            search_pattern = f"%{search_query}%"
            query = query.filter((Event.title.like(search_pattern)) | (Event.description.like(search_pattern)))
        
        if category_filter and category_filter != 'All':
            query = query.filter(Event.category == category_filter)
        
        # Sort by date
        query = query.order_by(Event.date.asc())
        
        return query.all()

    @staticmethod
    def get_past_events(user_id, search_query='', category_filter=''):
        """Fetch past events with filters"""
        today = str(date.today())
        
        query = Event.query.filter(Event.date < today)
        
        if search_query:
            search_pattern = f"%{search_query}%"
            query = query.filter((Event.title.like(search_pattern)) | (Event.description.like(search_pattern)))
        
        if category_filter and category_filter != 'All':
            query = query.filter(Event.category == category_filter)
        
        # Sort by date DESC logic for history
        query = query.order_by(Event.date.desc())
        
        return query.all()

    @staticmethod
    def get_all_categories():
        return [r.category for r in db.session.query(Event.category).distinct().order_by(Event.category).all() if r.category]

    @staticmethod
    def join_event(user_id, event_id):
        event = db.session.get(Event, event_id)
        if not event:
            return False, "Event not found"
            
        # Check if already joined
        participant = EventParticipant.query.filter_by(user_id=user_id, event_id=event_id).first()
        if participant:
            return False, "You already joined this event"
            
        # Check capacity
        current_count = EventParticipant.query.filter_by(event_id=event_id).count()
        if event.capacity and current_count >= event.capacity:
            return False, "Event is full"
            
        new_participant = EventParticipant(user_id=user_id, event_id=event_id)
        db.session.add(new_participant)
        db.session.commit()
        return True, "You have joined the event!"

    @staticmethod
    def leave_event(user_id, event_id):
        participant = EventParticipant.query.filter_by(user_id=user_id, event_id=event_id).first()
        if not participant:
            return False, "You are not part of this event"
            
        db.session.delete(participant)
        db.session.commit()
        return True, "You have left the event"

    @staticmethod
    def delete_event(user_id, event_id):
        event = Event.query.filter_by(id=event_id, user_id=user_id).first()
        if not event:
            return False, "Event not found or permission denied"
            
        # Cascade delete is handled by database ON DELETE CASCADE, but SQLAlchemy also handles it via relationships
        db.session.delete(event)
        db.session.commit()
        return True, "Event deleted successfully"

    @staticmethod
    def get_user_created_events(user_id):
        return Event.query.filter_by(user_id=user_id).order_by(Event.date.asc()).all()
        
    @staticmethod
    def get_user_joined_events(user_id):
        # Join-based query
        return Event.query.join(EventParticipant).filter(EventParticipant.user_id == user_id).order_by(Event.date.asc()).all()
