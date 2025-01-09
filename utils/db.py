import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    """Connect to the application's configured database."""
    if 'db' not in g:
        try:
            current_app.logger.debug("Attempting to connect to database")
            g.db = sqlite3.connect(
                current_app.config['DATABASE_PATH'],
                detect_types=sqlite3.PARSE_DECLTYPES,
                timeout=20,
                isolation_level=None  # This enables autocommit mode
            )
            g.db.execute('PRAGMA journal_mode=WAL')  # Use Write-Ahead Logging
            g.db.execute('PRAGMA busy_timeout=5000')  # Set busy timeout to 5 seconds
            g.db.row_factory = sqlite3.Row
            current_app.logger.debug("Successfully connected to database")
        except Exception as e:
            current_app.logger.error(f"Failed to connect to database: {str(e)}", exc_info=True)
            raise

    return g.db

def close_db(e=None):
    """Close the database connection."""
    db = g.pop('db', None)
    if db is not None:
        try:
            current_app.logger.debug("Closing database connection")
            db.close()
            current_app.logger.debug("Database connection closed successfully")
        except Exception as e:
            current_app.logger.error(f"Error closing database: {str(e)}", exc_info=True)

def init_db():
    """Initialize the database."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def add_message(content):
    """Add a new message to the database."""
    db = get_db()
    cursor = db.cursor()
    
    try:
        current_app.logger.debug(f"Attempting to insert message: {content}")
        cursor.execute(
            'INSERT INTO messages (content, synced) VALUES (?, ?)',
            (content, False)
        )
        db.commit()
        message_id = cursor.lastrowid
        current_app.logger.debug(f"Successfully inserted message with ID: {message_id}")
        return message_id
    except Exception as e:
        current_app.logger.error(f"Database error adding message: {str(e)}", exc_info=True)
        db.rollback()
        raise

def get_messages(limit=None):
    """Retrieve messages from the database."""
    db = get_db()
    try:
        current_app.logger.debug(f"Fetching messages with limit: {limit}")
        if limit:
            messages = db.execute(
                'SELECT * FROM messages ORDER BY created_at DESC LIMIT ?',
                (limit,)
            ).fetchall()
        else:
            messages = db.execute(
                'SELECT * FROM messages ORDER BY created_at DESC'
            ).fetchall()
        
        current_app.logger.debug(f"Retrieved {len(messages)} messages from database")
        return messages
    except Exception as e:
        current_app.logger.error(f"Database error retrieving messages: {str(e)}", exc_info=True)
        raise

def update_sync_status(message_id, commit_hash):
    """Update the sync status of a message."""
    db = get_db()
    try:
        current_app.logger.debug(f"Updating sync status for message ID: {message_id}")
        db.execute(
            'UPDATE messages SET synced = ?, git_commit_hash = ? WHERE id = ?',
            (True, commit_hash, message_id)
        )
        db.commit()
        current_app.logger.debug(f"Successfully updated sync status for message ID: {message_id}")
    except Exception as e:
        current_app.logger.error(f"Database error updating sync status: {str(e)}", exc_info=True)
        db.rollback()
        raise

def get_unsynced_messages():
    """Get all unsynced messages."""
    db = get_db()
    try:
        current_app.logger.debug("Fetching unsynced messages")
        return db.execute(
            'SELECT * FROM messages WHERE synced = ? ORDER BY created_at',
            (False,)
        ).fetchall()
    except Exception as e:
        current_app.logger.error(f"Database error retrieving unsynced messages: {str(e)}", exc_info=True)
        raise
