import os
from app import create_app

# Determine environment from FLASK_ENV variable
# Defaults to 'production' for safety
config_name = os.environ.get('FLASK_ENV', 'production')

# Create application instance
app = create_app(config_name)

if __name__ == "__main__":
    # This block is only used when running directly (not via WSGI server)
    # In production, Gunicorn/uWSGI will use the 'app' object directly
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(debug=debug_mode)
