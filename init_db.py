"""
Database Initialization Script
Creates the database schema if it doesn't exist
Safe to run multiple times - only creates tables if they don't exist
"""

import sqlite3
import os
from datetime import datetime


def init_database(db_path='orbit.db'):
    """Initialize database with all required tables"""
    
    # Check if database exists
    db_exists = os.path.exists(db_path)
    
    if not db_exists:
        print(f"📦 Creating new database: {db_path}")
    else:
        print(f"🔍 Database found: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Users table ready")
    
    # Create events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT,
            description TEXT,
            category TEXT DEFAULT 'General',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    print("✅ Events table ready")
    
    conn.commit()
    conn.close()
    
    if not db_exists:
        print("\n✨ Database created successfully!")
    else:
        print("\n✅ Database schema verified!")
    
    return True


if __name__ == "__main__":
    init_database()
