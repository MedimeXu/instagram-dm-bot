import sqlite3
from datetime import datetime

class ConversationDB:
    def __init__(self, db_path="conversations.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                username TEXT,
                first_seen DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def save_message(self, user_id, role, content):
        self.conn.execute(
            "INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)",
            (user_id, role, content)
        )
        self.conn.commit()

    def get_conversation(self, user_id, limit=20):
        cursor = self.conn.execute(
            "SELECT role, content, timestamp FROM messages WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (user_id, limit)
        )
        rows = [{"role": r["role"], "content": r["content"], "timestamp": r["timestamp"]} for r in cursor]
        return list(reversed(rows))

    def save_user_info(self, user_id, name, username):
        self.conn.execute(
            "INSERT OR REPLACE INTO users (user_id, name, username) VALUES (?, ?, ?)",
            (user_id, name, username)
        )
        self.conn.commit()

    def get_user_info(self, user_id):
        cursor = self.conn.execute(
            "SELECT name, username, first_seen FROM users WHERE user_id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        if row:
            return {"name": row["name"], "username": row["username"], "first_seen": row["first_seen"]}
        return None

    def close(self):
        self.conn.close()
