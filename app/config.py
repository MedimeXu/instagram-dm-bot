# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.META_VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "")
        self.META_PAGE_ACCESS_TOKEN = os.getenv("META_PAGE_ACCESS_TOKEN", "")
        self.META_APP_SECRET = os.getenv("META_APP_SECRET", "")
        self.INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "")
        self.TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.TELEGRAM_ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID", "")
        self.AUTO_MODE = os.getenv("AUTO_MODE", "false").lower() == "true"
        self.FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
        self.DATABASE_PATH = os.getenv("DATABASE_PATH", "conversations.db")
        self.CLAUDE_MODE = os.getenv("CLAUDE_MODE", "cli")
        self.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

    def toggle_auto_mode(self):
        self.AUTO_MODE = not self.AUTO_MODE

config = Config()
