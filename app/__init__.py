from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from config import config

# Initialize extensions
session_manager = Session()
flask_db = SQLAlchemy()


class DBWrapper:
    """
    Compatibility wrapper to make Flask-SQLAlchemy look like cs50.SQL.
    This allows us to transition to SQLAlchemy connection pooling without
    rewriting every single query in the application immediately.
    """
    def __init__(self):
        self._session = None

    def init_session(self, session):
        self._session = session

    def execute(self, sql, *args):
        """
        Executes a raw SQL query with optional parameters.
        Supports '?' placeholders (SQLite style) by converting them to bound parameters.
        Also handles basic dialect incompatibilities like GROUP_CONCAT vs STRING_AGG.
        """
        if self._session is None:
             raise RuntimeError("Database session not initialized. DBWrapper.init_session() must be called.")

        # 1. Convert '?' placeholders to SQLAlchemy bound parameters (:p0, :p1, etc.)
        if '?' in sql:
            parts = sql.split('?')
            converted_sql = ""
            for i, part in enumerate(parts[:-1]):
                converted_sql += f"{part}:p{i}"
            converted_sql += parts[-1]
            sql = converted_sql
            
            # Create a dictionary of parameters
            params = {f'p{i}': arg for i, arg in enumerate(args)}
        else:
            # Handle named parameters if used or if no args are provided
            params = {}

        # 2. Handle Dialect-Specific SQL Replacements
        try:
            db_engine = self._session.get_bind().dialect.name
            import sys
            print(f"DEBUG: DB Engine: {db_engine}", file=sys.stderr)
            
            if 'postgres' in db_engine:
                # Postgres uses STRING_AGG(field, ', ') instead of GROUP_CONCAT(field, ', ')
                # Simple string replacement for the common case in this app
                sql = sql.replace('GROUP_CONCAT', 'STRING_AGG')
            
            print(f"DEBUG: Executing SQL: {sql} with params: {params}", file=sys.stderr)

            # 3. Execute the query
            result = self._session.execute(text(sql), params)
            
            # 4. Commit the transaction automatically (replicating cs50 behavior)
            self._session.commit()

            # 5. Return results based on query type
            if result.returns_rows:
                # Return list of dicts (cs50 style)
                # mappings() is available in newer SQLAlchemy
                return [dict(row) for row in result.mappings().all()]
            else:
                # For INSERT/UPDATE/DELETE, return rowcount or primary key (if insert)
                return result.rowcount

        except Exception as e:
            import sys
            print(f"ERROR in DBWrapper: {e}", file=sys.stderr)
            self._session.rollback()
            raise e


# Global database instance (Compatibility Wrapper)
# Instantiated here so imports get this object. Session injected later.
db = DBWrapper()


def create_app(config_name='default'):
    """Application Factory Pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    session_manager.init_app(app)
    flask_db.init_app(app)
    
    # Initialize compatibility wrapper session
    with app.app_context():
        db.init_session(flask_db.session)
    
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

    # NOTE: 'cleanup_old_events' removed for performance. 
    # To be replaced by a background job in future phases.

    return app
