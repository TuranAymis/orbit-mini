-- 1. Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create events table
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT,
    description TEXT,
    category TEXT DEFAULT 'General',
    capacity INTEGER,
    location TEXT,
    location_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 3. Create participants table
CREATE TABLE IF NOT EXISTS event_participants (
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, event_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

-- 4. Seed Admin User
-- Password is 'admin123'
INSERT INTO users (username, hash)
VALUES ('admin@admin.com', 'scrypt:32768:8:1$NAk0qYkEoFD99KjF$98e323a756fd496c188722a8bdd87b92c6219d4558fd34fb292380af4fb40d95abd4859146b4455fba4c6838e3cea81db4a90e8058f20179be40f15f2289b82a')
ON CONFLICT (username) DO NOTHING;
