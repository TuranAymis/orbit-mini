import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection():
    db_url = os.environ.get('DATABASE_URL')
    
    if not db_url or db_url.startswith('sqlite'):
        if not db_url:
            project_root = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(project_root, 'orbit.db')
        else:
            db_path = db_url.replace('sqlite:///', '')
            
        print(f"Using SQLite database: {db_path}")
        return sqlite3.connect(db_path), 'sqlite'

    elif db_url.startswith('postgres'):
        try:
            import psycopg2
        except ImportError:
            print("❌ psycopg2 not installed.")
            return None, None
            
        print("Using PostgreSQL database...")
        # Handle SQLAlchemy URL format if necessary for raw psycopg2
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
            
        return psycopg2.connect(db_url), 'postgres'

    return None, None

def migrate_database():
    conn, db_type = get_db_connection()
    if not conn:
        print("❌ Could not connect to database.")
        return

    cursor = conn.cursor()
    print(f"📦 Migrating database ({db_type})...")

    try:
        # 1. Add image_url to events table
        print("1. Adding image_url to events table...")
        if db_type == 'sqlite':
            # Check if column exists first to avoid error
            try:
                cursor.execute("SELECT image_url FROM events LIMIT 1")
                print("   - Column image_url already exists.")
            except:
                cursor.execute("ALTER TABLE events ADD COLUMN image_url TEXT")
                print("   - Added image_url column.")
        else: # Postgres
             # Check if column exists
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='events' AND column_name='image_url'")
            if cursor.fetchone():
                print("   - Column image_url already exists.")
            else:
                cursor.execute("ALTER TABLE events ADD COLUMN image_url TEXT")
                print("   - Added image_url column.")

        # 2. Create comments table
        print("2. Creating comments table...")
        
        # Define types
        if db_type == 'postgres':
            pk_type = "SERIAL PRIMARY KEY"
            text_type = "TEXT"
            timestamp_default = "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        else:
            pk_type = "INTEGER PRIMARY KEY AUTOINCREMENT"
            text_type = "TEXT"
            timestamp_default = "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS comments (
                id {pk_type},
                content {text_type} NOT NULL,
                user_id INTEGER NOT NULL,
                event_id INTEGER NOT NULL,
                created_at {timestamp_default},
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
            )
        """)
        print("   - Verified/Created comments table.")

        conn.commit()
        print("✅ Migration completed successfully!")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
