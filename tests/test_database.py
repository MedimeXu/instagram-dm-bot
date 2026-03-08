import pytest
import os
from app.database import ConversationDB

@pytest.fixture
def db(tmp_path):
    db_path = str(tmp_path / "test.db")
    database = ConversationDB(db_path)
    yield database
    database.close()

def test_save_and_get_messages(db):
    db.save_message("user_123", "incoming", "Salut !")
    db.save_message("user_123", "outgoing", "Hello ! \ud83d\ude0a")

    history = db.get_conversation("user_123")
    assert len(history) == 2
    assert history[0]["role"] == "incoming"
    assert history[0]["content"] == "Salut !"
    assert history[1]["role"] == "outgoing"
    assert history[1]["content"] == "Hello ! \ud83d\ude0a"

def test_get_conversation_limit(db):
    for i in range(25):
        db.save_message("user_456", "incoming", f"Message {i}")

    history = db.get_conversation("user_456", limit=10)
    assert len(history) == 10

def test_separate_conversations(db):
    db.save_message("user_A", "incoming", "Bonjour A")
    db.save_message("user_B", "incoming", "Bonjour B")

    history_a = db.get_conversation("user_A")
    assert len(history_a) == 1
    assert history_a[0]["content"] == "Bonjour A"

def test_get_user_info(db):
    db.save_user_info("user_123", "Lisa", "lisa_insta")
    info = db.get_user_info("user_123")
    assert info["name"] == "Lisa"
    assert info["username"] == "lisa_insta"
