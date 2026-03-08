import requests
import hmac
import hashlib

class InstagramClient:
    BASE_URL = "https://graph.instagram.com/v21.0"

    def __init__(self, page_access_token, app_secret, ig_account_id):
        self.token = page_access_token
        self.app_secret = app_secret
        self.ig_account_id = ig_account_id

    def send_message(self, recipient_id, text):
        url = f"{self.BASE_URL}/me/messages"
        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": text}
        }
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(url, json=payload, headers=headers)
        return response.status_code == 200

    def send_multiple_messages(self, recipient_id, messages):
        results = []
        for msg in messages:
            results.append(self.send_message(recipient_id, msg))
        return all(results)

    def parse_webhook(self, payload):
        messages = []
        for entry in payload.get("entry", []):
            for event in entry.get("messaging", []):
                if "message" in event and "text" in event["message"]:
                    messages.append({
                        "sender_id": event["sender"]["id"],
                        "text": event["message"]["text"],
                        "message_id": event["message"].get("mid", "")
                    })
        return messages

    def get_user_profile(self, user_id):
        url = f"{self.BASE_URL}/{user_id}"
        params = {"fields": "name,username", "access_token": self.token}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return {"name": "Inconnu", "username": "inconnu"}

    def verify_signature(self, payload_body, signature):
        expected = hmac.HMAC(
            self.app_secret.encode(),
            payload_body,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(f"sha256={expected}", signature)
