"""Production configuration."""
import os
from config import Config

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Rate limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = "memory://"
    
    # Database
    DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'bookchat.db')
    
    # GitHub sync
    SYNC_INTERVAL = 300  # 5 minutes
    
    # Message settings
    MAX_MESSAGE_LENGTH = 1000
    MESSAGES_PER_PAGE = 50
