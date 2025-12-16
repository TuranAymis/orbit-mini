"""
Database Initialization Script
Creates the database with the correct schema for both SQLite and PostgreSQL.
"""

import sqlite3
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection(db_url=None):
    """
    Returns a database connection and type ('sqlite' or 'postgres').
    If db_url is provided, it is used. Otherwise, it looks for DATABASE_URL.
    Default fallback is local SQLite 'orbit.db'.
    """
    if not db_url:
        db_url = os.environ.get('DATABASE_URL')

    # SQLite
    if not db_url or db_url.startswith('sqlite'):
        if not db_url:
            project_root = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(project_root, 'orbit.db')
        else:
            db_path = db_url.replace('sqlite:///', '')
            
        print(f"Using SQLite database: {db_path}")
        return sqlite3.connect(db_path), 'sqlite'

    # PostgreSQL
    elif db_url.startswith('postgres'):
        try:
            import psycopg2
        except ImportError:
            print("❌ psycopg2 not installed. Please install it: pip install psycopg2-binary")
            sys.exit(1)
            
        print("Using PostgreSQL database...")
        # Fix for SQLAlchemy style postgres:// URLs if used with psycopg2 directly (though libraries usually handle it, raw psycopg2 wants postgresql://)
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
            
        return psycopg2.connect(db_url), 'postgres'

    else:
        raise ValueError(f"Unsupported database URL: {db_url}")


def init_database(reset=False):
    """Initialize database with all required tables"""
    
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    
    print("📦 Setting up schema...")
    
    # Define SQL types based on DB engine
    if db_type == 'postgres':
        primary_key_type = "SERIAL PRIMARY KEY" # or GENERATED ALWAYS AS IDENTITY in newer PG
        text_type = "TEXT"
    else:
        primary_key_type = "INTEGER PRIMARY KEY AUTOINCREMENT"
        text_type = "TEXT"

    # Create users table
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS users (
            id {primary_key_type},
            username {text_type} UNIQUE NOT NULL,
            hash {text_type} NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create events table
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS events (
            id {primary_key_type},
            user_id INTEGER NOT NULL,
            title {text_type} NOT NULL,
            date {text_type} NOT NULL,
            time {text_type},
            description {text_type},
            category {text_type} DEFAULT 'General',
            capacity INTEGER,
            location {text_type},
            location_name {text_type},
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Create participants table (Join table)
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS event_participants (
            user_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, event_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database schema created successfully in {db_type}!")
    return True


if __name__ == "__main__":
    init_database()
