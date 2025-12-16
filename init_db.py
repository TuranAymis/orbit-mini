"""
Database Initialization Script
Creates the database with the correct schema.
WARNING: This script will DELETE existing data if reset=True (default when run as script).
"""

import sqlite3
import os
import sys

def init_database(db_path='orbit.db', reset=False):
    """Initialize database with all required tables"""
    
    # Nuclear Option: Delete existing database if reset requested
    if reset and os.path.exists(db_path):
        print(f"☢️  NUCLEAR OPTION: Deleting existing database: {db_path}")
        try:
            os.remove(db_path)
            print("🗑️  Database deleted successfully")
        except PermissionError:
            print(f"❌ Error: Could not delete {db_path}. Is it open in another program?")
            return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("📦 Setting up schema...")

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create events table with all fields
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT,
            description TEXT,
            category TEXT DEFAULT 'General',
            capacity INTEGER,
            location TEXT,
            location_name TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Create participants table (Join table)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS event_participants (
            user_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, event_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    conn.close()
    
    print("✅ Database schema created successfully (users, events, event_participants)!")
    return True


if __name__ == "__main__":
    # If run directly, assume we want to reset (or check arg)
    reset_mode = True
    project_root = os.path.dirname(os.path.abspath(__file__))
    db_file = os.path.join(project_root, 'orbit.db')
    
    init_database(db_path=db_file, reset=reset_mode)
