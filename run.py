import os
from app import create_app

# Determine environment
config_name = os.environ.get('FLASK_ENV', 'production')

# Create application instance
app = create_app(config_name)

if __name__ == '__main__':
    # Debug mode controlled by environment variable, defaults to False for safety
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(debug=debug_mode)
