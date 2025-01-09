import logging
from logging.handlers import RotatingFileHandler
import os

def init_logger(app):
    """Initialize application logger."""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Set up file handler
    file_handler = RotatingFileHandler(
        'logs/bookchat.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    
    # Set formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)

    # Set log level based on environment
    if app.debug:
        file_handler.setLevel(logging.DEBUG)
    else:
        file_handler.setLevel(logging.INFO)

    # Add handler to app logger
    app.logger.addHandler(file_handler)

    # Remove default handler
    app.logger.removeHandler(app.logger.handlers[0])

    return app.logger
