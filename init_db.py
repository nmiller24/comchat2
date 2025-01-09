from app import create_app
import sqlite3
import os
import time

def init_db():
    app = create_app()
    
    with app.app_context():
        # Get database path from config
        db_path = app.config['DATABASE_PATH']
        
        # Create database directory if it doesn't exist
        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        # Try to connect to database with retries
        max_retries = 5
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                # Connect to database and create tables
                with sqlite3.connect(db_path, timeout=20) as conn:
                    with open('schema.sql', 'r') as f:
                        conn.executescript(f.read())
                    
                    print(f"Database initialized at {db_path}")
                    return True
                    
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    if attempt < max_retries - 1:
                        print(f"Database is locked, retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                        continue
                raise
            except Exception as e:
                print(f"Error initializing database: {str(e)}")
                raise
        
        return False

if __name__ == '__main__':
    init_db()
