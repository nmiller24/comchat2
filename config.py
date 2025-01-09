import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    PORT = int(os.getenv('PORT', 5009))
    DEBUG = FLASK_ENV == 'development'
    
    # GitHub configuration
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    
    # Database configuration
    DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bookchat.db')
    
    # Rate limiting
    RATELIMIT_DEFAULT = "100 per minute"
    RATELIMIT_STORAGE_URL = "memory://"
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())
    
    # GitHub sync configuration
    SYNC_INTERVAL = 300  # 5 minutes
    COMMIT_MESSAGE_PREFIX = "[BookChat]"
    
    # Message configuration
    MAX_MESSAGE_LENGTH = 1000
    MESSAGES_PER_PAGE = 50
    
    @staticmethod
    def init_app(app):
        """Initialize application configuration"""
        app.config.from_object(__name__ + '.Config')
