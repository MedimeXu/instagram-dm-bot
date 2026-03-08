import pytest
from unittest.mock import patch, MagicMock
from app.instagram import InstagramClient

@pytest.fixture
def ig_client():
    return InstagramClient(
        page_access_token="test_token",
        app_secret="test_secret",
        ig_account_id="test_id"
    )

def test_send_message(ig_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"recipient_id": "123", "message_id": "mid.xxx"}

    with patch("requests.post", return_value=mock_response) as mock_post:
        result = ig_client.send_message("123", "Hello !")
        assert result is True
        mock_post.assert_called_once()

def test_parse_webhook_message(ig_client):
    payload = {
        "entry": [{
            "messaging": [{
                "sender": {"id": "sender_123"},
                "message": {"text": "Salut Juliette !"}
            }]
        }]
    }

    messages = ig_client.parse_webhook(payload)
    assert len(messages) == 1
    assert messages[0]["sender_id"] == "sender_123"
    assert messages[0]["text"] == "Salut Juliette !"

def test_parse_webhook_no_message(ig_client):
    payload = {"entry": [{"messaging": [{"sender": {"id": "123"}, "delivery": {}}]}]}
    messages = ig_client.parse_webhook(payload)
    assert len(messages) == 0

def test_get_user_profile(ig_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"name": "Lisa", "username": "lisa_beauty"}

    with patch("requests.get", return_value=mock_response) as mock_get:
        profile = ig_client.get_user_profile("123")
        assert profile["name"] == "Lisa"
