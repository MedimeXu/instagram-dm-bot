# tests/test_config.py
import os
import pytest

def test_config_loads_env_vars(monkeypatch):
    monkeypatch.setenv("META_VERIFY_TOKEN", "test_token")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "tg_token")
    monkeypatch.setenv("TELEGRAM_ADMIN_CHAT_ID", "12345")
    monkeypatch.setenv("AUTO_MODE", "false")

    from app.config import Config
    config = Config()

    assert config.META_VERIFY_TOKEN == "test_token"
    assert config.TELEGRAM_BOT_TOKEN == "tg_token"
    assert config.TELEGRAM_ADMIN_CHAT_ID == "12345"
    assert config.AUTO_MODE is False

def test_auto_mode_toggle():
    from app.config import Config
    config = Config()
    config.AUTO_MODE = False

    config.toggle_auto_mode()
    assert config.AUTO_MODE is True

    config.toggle_auto_mode()
    assert config.AUTO_MODE is False
