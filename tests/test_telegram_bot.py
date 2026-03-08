from app.telegram_bot import TelegramValidator

def test_format_validation_message():
    validator = TelegramValidator(bot_token="test", admin_chat_id="12345")

    formatted = validator.format_validation_message(
        username="lisa_beauty",
        incoming_message="C'est quoi la m\u00e9thode low ticket ?",
        suggested_replies=["Hello ! \ud83d\ude0a", "En gros c'est une formation pas \u00e0 pas..."]
    )

    assert "lisa_beauty" in formatted
    assert "C'est quoi la m\u00e9thode low ticket ?" in formatted
    assert "Hello ! \ud83d\ude0a" in formatted
    assert "APPROUVER" in formatted or "approuver" in formatted.lower() or "Que veux-tu faire" in formatted

def test_format_auto_mode_notification():
    validator = TelegramValidator(bot_token="test", admin_chat_id="12345")

    formatted = validator.format_auto_notification(
        username="lisa_beauty",
        incoming_message="Salut !",
        sent_replies=["Hello \ud83d\ude0a", "T'es dans quoi ?"]
    )

    assert "AUTO" in formatted or "auto" in formatted.lower()
    assert "lisa_beauty" in formatted

def test_parse_callback_approve():
    validator = TelegramValidator(bot_token="test", admin_chat_id="12345")

    result = validator.parse_callback("approve:sender_123:msg_456")
    assert result["action"] == "approve"
    assert result["sender_id"] == "sender_123"

def test_parse_callback_reject():
    validator = TelegramValidator(bot_token="test", admin_chat_id="12345")

    result = validator.parse_callback("reject:sender_123:msg_456")
    assert result["action"] == "reject"
