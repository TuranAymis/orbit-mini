#!/usr/bin/env python3
"""
Startup script for production deployment
Ensures database is initialized before starting the application
"""

import os
import sys
from init_db import init_database

def startup():
    """Initialize database and prepare for production"""
    print("🚀 Starting Orbit Mini...")
    
    # Get database path from environment or use default
    db_path = os.environ.get('DATABASE_URL', 'sqlite:///orbit.db')
    if db_path.startswith('sqlite:///'):
        db_path = db_path.replace('sqlite:///', '')
    
    # Initialize database
    try:
        init_database(db_path)
        print("✅ Database ready")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)
    
    print("✅ Startup complete!")
    return True

if __name__ == "__main__":
    startup()
