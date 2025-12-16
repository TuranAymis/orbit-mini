from flask import Flask
from flask_session import Session
from cs50 import SQL
from config import config


# Global database instance
db = None
session_manager = Session()


def create_app(config_name='default'):
    """Application Factory Pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    session_manager.init_app(app)
    
    # Initialize database
    global db
    db_uri = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', 'sqlite:///')
    db = SQL(db_uri)
    
    # Register blueprints
    from app.auth import auth_bp
    from app.events import events_bp
    from app.main import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(main_bp)
    
    # Cache control headers
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    # Auto-cleanup: Delete events older than 3 days
    @app.before_request
    def cleanup_old_events():
        try:
            # 1. Delete participants of expired events
            db.execute("""
                DELETE FROM event_participants 
                WHERE event_id IN (
                    SELECT id FROM events 
                    WHERE date < DATE('now', '-3 days')
                )
            """)
            
            # 2. Delete the expired events
            db.execute("DELETE FROM events WHERE date < DATE('now', '-3 days')")
        except Exception as e:
            # Log error but don't stop the request
            print(f"Cleanup error: {e}")
            pass

    return app
