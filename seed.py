import sys
import os

# Ensure the app module can be found
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import app as application_module 
from werkzeug.security import generate_password_hash

def seed():
    # Initialize the app which sets up the database connection
    flask_app = application_module.create_app()
    
    print("🌱 Seeding database...")
    
    # User details
    username = "admin@admin.com" # Using email as username
    password = "admin123"
    
    print(f"   Target User: {username}")
    
    # generate_password_hash default method is usually pbkdf2:sha256 in newer werkzeug
    hashed_password = generate_password_hash(password)
    
    # Check if user exists
    try:
        # Access db from the module where it was initialized
        db = application_module.db
        
        if db is None:
            print("❌ Error: Database connection (db) is still None after create_app().")
            return

        existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)
        
        if existing_user:
            print(f"⚠️ User '{username}' already exists. Updating password...")
            db.execute("UPDATE users SET hash = ? WHERE username = ?", hashed_password, username)
        else:
            print(f"👤 Creating user '{username}'...")
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)
            
        print("✅ Seeding completed successfully!")
        print("ℹ️  Note: 'role' field was skipped as it does not exist in the 'users' table schema.")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")

if __name__ == "__main__":
    seed()
