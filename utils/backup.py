import os
import shutil
import sqlite3
from datetime import datetime
from flask import current_app

class BackupManager:
    def __init__(self, backup_dir='backups'):
        self.backup_dir = backup_dir
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

    def create_backup(self):
        """Create a backup of the database."""
        try:
            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(
                self.backup_dir,
                f'bookchat_backup_{timestamp}.db'
            )

            # Create backup using SQLite's backup API
            with sqlite3.connect(current_app.config['DATABASE_PATH']) as src:
                with sqlite3.connect(backup_path) as dst:
                    src.backup(dst)

            current_app.logger.info(f"Database backup created: {backup_path}")
            return backup_path

        except Exception as e:
            current_app.logger.error(f"Backup creation failed: {str(e)}")
            raise

    def restore_backup(self, backup_path):
        """Restore database from backup."""
        try:
            if not os.path.exists(backup_path):
                raise FileNotFoundError(f"Backup file not found: {backup_path}")

            # Create a temporary copy of the current database
            temp_backup = f"{current_app.config['DATABASE_PATH']}.temp"
            shutil.copy2(current_app.config['DATABASE_PATH'], temp_backup)

            try:
                # Restore from backup
                with sqlite3.connect(backup_path) as src:
                    with sqlite3.connect(current_app.config['DATABASE_PATH']) as dst:
                        src.backup(dst)

                current_app.logger.info(f"Database restored from: {backup_path}")
                os.remove(temp_backup)
                return True

            except Exception as e:
                # If restoration fails, restore from temporary backup
                shutil.copy2(temp_backup, current_app.config['DATABASE_PATH'])
                os.remove(temp_backup)
                raise Exception(f"Restore failed: {str(e)}")

        except Exception as e:
            current_app.logger.error(f"Restore failed: {str(e)}")
            raise

    def list_backups(self):
        """List all available backups."""
        try:
            backups = []
            for file in os.listdir(self.backup_dir):
                if file.startswith('bookchat_backup_') and file.endswith('.db'):
                    backup_path = os.path.join(self.backup_dir, file)
                    backup_time = datetime.strptime(
                        file[16:-3],
                        '%Y%m%d_%H%M%S'
                    )
                    backups.append({
                        'path': backup_path,
                        'timestamp': backup_time,
                        'size': os.path.getsize(backup_path)
                    })
            return sorted(backups, key=lambda x: x['timestamp'], reverse=True)

        except Exception as e:
            current_app.logger.error(f"Error listing backups: {str(e)}")
            raise

    def cleanup_old_backups(self, keep_count=10):
        """Remove old backups, keeping only the specified number of recent ones."""
        try:
            backups = self.list_backups()
            if len(backups) > keep_count:
                for backup in backups[keep_count:]:
                    os.remove(backup['path'])
                    current_app.logger.info(
                        f"Removed old backup: {backup['path']}"
                    )
        except Exception as e:
            current_app.logger.error(f"Backup cleanup failed: {str(e)}")
            raise
