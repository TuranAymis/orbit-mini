from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from config import config

# Initialize extensions
session_manager = Session()
db = SQLAlchemy()


def create_app(config_name='default'):
    """Application Factory Pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    session_manager.init_app(app)
    db.init_app(app)
    from flask_wtf.csrf import CSRFProtect
    csrf = CSRFProtect(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.events import events_bp
    from app.routes.main import main_bp
    
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

    return app

