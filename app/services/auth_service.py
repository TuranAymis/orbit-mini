from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.models import User

class AuthService:
    @staticmethod
    def register_user(username, password):
        """
        Registers a new user.
        Returns the new user object or None if username exists.
        """
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return None # Username taken
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, hash=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def authenticate_user(username, password):
        """
        Authenticates a user.
        Returns the user object if successful, else None.
        """
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.hash, password):
            return user
        return None

    @staticmethod
    def get_user_by_id(user_id):
        return db.session.get(User, user_id)
