"""
Database Migration Script
Adds new columns to events table: time, category, created_at
Preserves all existing data
"""

import sqlite3
from datetime import datetime

def migrate_database():
    """Add new columns to events table"""
    
    conn = sqlite3.connect('orbit.db')
    cursor = conn.cursor()
    
    print("🔄 Starting database migration...")
    
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(events)")
    columns = [column[1] for column in cursor.fetchall()]
    
    migrations_needed = []
    
    # Add 'time' column if it doesn't exist
    if 'time' not in columns:
        migrations_needed.append(('time', "ALTER TABLE events ADD COLUMN time TEXT"))
    
    # Add 'category' column if it doesn't exist
    if 'category' not in columns:
        migrations_needed.append(('category', "ALTER TABLE events ADD COLUMN category TEXT DEFAULT 'General'"))
    
    # Add 'created_at' column if it doesn't exist (SQLite doesn't support CURRENT_TIMESTAMP in ALTER TABLE)
    if 'created_at' not in columns:
        migrations_needed.append(('created_at', "ALTER TABLE events ADD COLUMN created_at DATETIME"))
    
    if not migrations_needed:
        print("✅ Database is already up to date!")
        conn.close()
        return
    
    # Execute migrations
    for column_name, sql in migrations_needed:
        try:
            cursor.execute(sql)
            print(f"✅ Added column: {column_name}")
        except sqlite3.OperationalError as e:
            print(f"⚠️  Column {column_name} might already exist: {e}")
    
    # Update existing events with timestamps
    try:
        cursor.execute("""
            UPDATE events 
            SET created_at = CURRENT_TIMESTAMP 
            WHERE created_at IS NULL
        """)
        print("✅ Updated existing events with timestamps")
    except sqlite3.OperationalError as e:
        print(f"⚠️  Could not update timestamps: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Database migration completed successfully!")
    print("\nNew schema:")
    print("  - time: Event time (e.g., '14:30')")
    print("  - category: Event category (Tech, Social, Sports, Art, etc.)")
    print("  - created_at: Timestamp when event was created")


if __name__ == "__main__":
    migrate_database()
