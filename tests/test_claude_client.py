import pytest
from unittest.mock import patch, MagicMock
from app.claude_client import ClaudeClient

def test_generate_response_cli_mode():
    client = ClaudeClient(mode="cli")

    mock_result = MagicMock()
    mock_result.stdout = "Merci beaucoup \ud83e\udd0d\n---\nT'es dans quoi toi en ce moment ?"
    mock_result.returncode = 0

    with patch("subprocess.run", return_value=mock_result) as mock_run:
        response = client.generate_response("system prompt", "user message")
        assert "Merci" in response
        mock_run.assert_called_once()

def test_generate_response_api_mode():
    client = ClaudeClient(mode="api", api_key="test-key")

    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="Hello \ud83d\ude0a\n---\nComment tu vas ?")]

    mock_anthropic = MagicMock()
    mock_client_instance = MagicMock()
    mock_client_instance.messages.create.return_value = mock_message
    mock_anthropic.Anthropic.return_value = mock_client_instance

    import sys
    with patch.dict(sys.modules, {"anthropic": mock_anthropic}):
        client = ClaudeClient(mode="api", api_key="test-key")
        response = client.generate_response("system prompt", "user message")
        assert "Hello" in response

def test_parse_multiple_messages():
    client = ClaudeClient(mode="cli")
    messages = client.parse_bubbles("Salut \ud83d\ude0a\n---\nComment \u00e7a va ?\n---\nDis-moi tout")
    assert len(messages) == 3
    assert messages[0] == "Salut \ud83d\ude0a"
    assert messages[1] == "Comment \u00e7a va ?"
    assert messages[2] == "Dis-moi tout"
