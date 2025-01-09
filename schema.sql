DROP TABLE IF EXISTS messages;

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    git_commit_hash TEXT,
    synced BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_created_at ON messages(created_at);
CREATE INDEX idx_synced ON messages(synced);
