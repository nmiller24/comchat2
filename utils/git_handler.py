import json
from datetime import datetime
from github import Github
from flask import current_app
from .db import get_unsynced_messages, update_sync_status

class GitHubHandler:
    def __init__(self, token):
        self.github = Github(token)
        self.repo = None
        self._initialize_repo()

    def _initialize_repo(self):
        """Initialize GitHub repository connection."""
        try:
            user = self.github.get_user()
            repo_name = "bookchat-messages"
            
            try:
                self.repo = user.get_repo(repo_name)
            except Exception:
                self.repo = user.create_repo(
                    repo_name,
                    description="BookChat message storage",
                    private=True
                )
        except Exception as e:
            current_app.logger.error(f"Failed to initialize GitHub repo: {str(e)}")
            raise

    def sync_messages(self):
        """Sync unsynced messages to GitHub."""
        try:
            unsynced_messages = get_unsynced_messages()
            if not unsynced_messages:
                return
            
            # Prepare message data
            messages_data = []
            for msg in unsynced_messages:
                messages_data.append({
                    'id': msg['id'],
                    'content': msg['content'],
                    'created_at': msg['created_at'].isoformat(),
                })
            
            # Create commit message
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            commit_message = f"{current_app.config['COMMIT_MESSAGE_PREFIX']} Sync messages - {timestamp}"
            
            # Create or update file in GitHub
            file_path = f"messages/{timestamp}.json"
            file_content = json.dumps(messages_data, indent=2)
            
            try:
                # Try to create new file
                commit = self.repo.create_file(
                    file_path,
                    commit_message,
                    file_content
                )
                commit_hash = commit['commit'].sha
            except Exception as e:
                current_app.logger.error(f"Failed to sync messages to GitHub: {str(e)}")
                return
            
            # Update sync status for all messages
            for msg in unsynced_messages:
                update_sync_status(msg['id'], commit_hash)
                
            return commit_hash
            
        except Exception as e:
            current_app.logger.error(f"Error in sync_messages: {str(e)}")
            raise

    def verify_connection(self):
        """Verify GitHub connection is working."""
        try:
            self.github.get_user().login
            return True
        except Exception:
            return False
