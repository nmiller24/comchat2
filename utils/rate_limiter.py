from flask import request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def init_limiter(app):
    """Initialize rate limiter."""
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["100 per minute"],
        storage_uri=app.config['RATELIMIT_STORAGE_URL']
    )
    return limiter
