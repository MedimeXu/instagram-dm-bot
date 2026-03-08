from app.prompts import build_system_prompt, build_user_message

def test_system_prompt_contains_identity():
    prompt = build_system_prompt()
    assert "Juliette" in prompt
    assert "@_julietteeva" in prompt
    assert "tu " in prompt.lower() or "tutoiement" in prompt.lower()

def test_build_user_message_with_history():
    history = [
        {"role": "incoming", "content": "Salut !"},
        {"role": "outgoing", "content": "Hello \ud83d\ude0a"},
    ]
    new_message = "C'est quoi la m\u00e9thode low ticket ?"
    username = "lisa_beauty"

    result = build_user_message(history, new_message, username)
    assert "lisa_beauty" in result
    assert "Salut !" in result
    assert "C'est quoi la m\u00e9thode low ticket ?" in result

def test_build_user_message_no_history():
    result = build_user_message([], "Bonjour !", "newuser")
    assert "Premier contact" in result or "premier" in result.lower()
    assert "Bonjour !" in result
