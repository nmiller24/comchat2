import psutil
import time
from flask import current_app
from .db import get_db

class SystemMonitor:
    def __init__(self):
        self.start_time = time.time()

    def get_system_stats(self):
        """Get system statistics."""
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_usage': psutil.virtual_memory().percent,
            'uptime': time.time() - self.start_time
        }

    def get_app_stats(self):
        """Get application statistics."""
        try:
            db = get_db()
            cursor = db.cursor()
            
            # Get total message count
            total_messages = cursor.execute(
                'SELECT COUNT(*) FROM messages'
            ).fetchone()[0]
            
            # Get unsynced message count
            unsynced_messages = cursor.execute(
                'SELECT COUNT(*) FROM messages WHERE synced = ?',
                (False,)
            ).fetchone()[0]
            
            # Get last message timestamp
            last_message = cursor.execute(
                'SELECT created_at FROM messages ORDER BY created_at DESC LIMIT 1'
            ).fetchone()
            
            return {
                'total_messages': total_messages,
                'unsynced_messages': unsynced_messages,
                'last_message_time': last_message[0] if last_message else None
            }
        except Exception as e:
            current_app.logger.error(f"Error getting app stats: {str(e)}")
            return None

    def get_all_stats(self):
        """Get all monitoring statistics."""
        return {
            'system': self.get_system_stats(),
            'application': self.get_app_stats()
        }
