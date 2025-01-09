from flask import Flask, request, jsonify, render_template, current_app
from flask_cors import CORS
import threading
import time
from config import Config
from utils.db import init_app as init_db, get_messages, add_message
from utils.git_handler import GitHubHandler
from utils.rate_limiter import init_limiter
from utils.logger import init_logger
from utils.monitor import SystemMonitor
from utils.backup import BackupManager

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    Config.init_app(app)
    
    # Initialize extensions
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:5009", "http://127.0.0.1:5009"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    init_db(app)
    limiter = init_limiter(app)
    init_logger(app)
    
    # Initialize monitoring and backup
    monitor = SystemMonitor()
    backup_manager = BackupManager()
    
    with app.app_context():
        # Initialize GitHub handler
        github_handler = GitHubHandler(app.config['GITHUB_TOKEN'])
        
        def sync_messages_periodically():
            """Background task to sync messages to GitHub."""
            with app.app_context():
                while True:
                    try:
                        app.logger.debug("Starting background sync")
                        github_handler.sync_messages()
                        app.logger.debug("Background sync completed successfully")
                    except Exception as e:
                        app.logger.error(f"Background sync failed: {str(e)}", exc_info=True)
                    time.sleep(app.config['SYNC_INTERVAL'])
        
        # Start background sync thread
        sync_thread = threading.Thread(target=sync_messages_periodically)
        sync_thread.daemon = True
        sync_thread.start()
    
    # Define rate limits for routes
    @limiter.limit("100 per minute")
    @app.route('/')
    def index():
        """Render the main application page."""
        return render_template('index.html')
    
    @limiter.limit("100 per minute")
    @app.route('/messages', methods=['GET'])
    def get_message_history():
        """Get message history."""
        try:
            app.logger.debug("Attempting to fetch messages")
            messages = get_messages(app.config['MESSAGES_PER_PAGE'])
            app.logger.debug(f"Retrieved {len(messages) if messages else 0} messages")
            return jsonify([dict(msg) for msg in messages])
        except Exception as e:
            app.logger.error(f"Error getting messages: {str(e)}")
            return jsonify({'error': 'Failed to retrieve messages'}), 500
    
    @limiter.limit("30 per minute")
    @app.route('/messages', methods=['POST'])
    def create_message():
        """Create a new message."""
        try:
            app.logger.debug("Received POST request to /messages")
            data = request.get_json()
            app.logger.debug(f"Request data: {data}")
            
            if not data or 'content' not in data:
                app.logger.warning("No content found in request")
                return jsonify({'error': 'Message content required'}), 400
                
            content = data['content'].strip()
            if not content:
                app.logger.warning("Empty content after stripping")
                return jsonify({'error': 'Message cannot be empty'}), 400
                
            if len(content) > app.config['MAX_MESSAGE_LENGTH']:
                app.logger.warning(f"Content length {len(content)} exceeds maximum {app.config['MAX_MESSAGE_LENGTH']}")
                return jsonify({'error': 'Message too long'}), 400
            
            app.logger.debug(f"Attempting to add message: {content}")
            message_id = add_message(content)
            app.logger.info(f"Successfully added message with ID: {message_id}")
            return jsonify({'id': message_id}), 201
            
        except Exception as e:
            app.logger.error(f"Error creating message: {str(e)}", exc_info=True)
            return jsonify({'error': 'Failed to create message'}), 500
    
    @limiter.limit("10 per minute")
    @app.route('/status')
    def get_status():
        """Get system status."""
        try:
            stats = monitor.get_all_stats()
            github_status = github_handler.verify_connection()
            
            return jsonify({
                'status': 'healthy',
                'github_connected': github_status,
                'stats': stats
            })
        except Exception as e:
            app.logger.error(f"Error getting status: {str(e)}")
            return jsonify({
                'status': 'unhealthy',
                'error': str(e)
            }), 500
    
    @app.errorhandler(429)
    def ratelimit_handler(e):
        """Handle rate limit exceeded."""
        return jsonify({
            'error': 'Rate limit exceeded',
            'retry_after': e.description
        }), 429
    
    @app.cli.command('create-backup')
    def create_backup_command():
        """Create a database backup."""
        try:
            backup_path = backup_manager.create_backup()
            print(f"Backup created: {backup_path}")
        except Exception as e:
            print(f"Backup failed: {str(e)}")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=5009,
        debug=app.config['DEBUG']
    )
