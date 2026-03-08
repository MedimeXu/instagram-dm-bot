import pytest
import json
from unittest.mock import patch, MagicMock

def test_webhook_verify():
    from app.webhook import create_app
    app = create_app(testing=True)
    client = app.test_client()

    response = client.get("/webhook?hub.mode=subscribe&hub.verify_token=test_verify&hub.challenge=challenge_123")
    assert response.status_code == 200
    assert response.data.decode() == "challenge_123"

def test_webhook_verify_wrong_token():
    from app.webhook import create_app
    app = create_app(testing=True)
    client = app.test_client()

    response = client.get("/webhook?hub.mode=subscribe&hub.verify_token=wrong&hub.challenge=challenge_123")
    assert response.status_code == 403

def test_webhook_receive_message():
    from app.webhook import create_app
    app = create_app(testing=True)
    client = app.test_client()

    payload = {
        "object": "instagram",
        "entry": [{
            "messaging": [{
                "sender": {"id": "sender_123"},
                "message": {"mid": "mid_123", "text": "Salut !"}
            }]
        }]
    }

    with patch("app.webhook.process_incoming_dm") as mock_process:
        response = client.post(
            "/webhook",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 200

def test_health_check():
    from app.webhook import create_app
    app = create_app(testing=True)
    client = app.test_client()

    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "ok"

def test_toggle_auto_mode():
    from app.webhook import create_app
    app = create_app(testing=True)
    client = app.test_client()

    response = client.post("/auto-mode/toggle")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "auto_mode" in data
