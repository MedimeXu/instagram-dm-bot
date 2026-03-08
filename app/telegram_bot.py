import json

class TelegramValidator:
    def __init__(self, bot_token, admin_chat_id):
        self.bot_token = bot_token
        self.admin_chat_id = admin_chat_id

    def format_validation_message(self, username, incoming_message, suggested_replies):
        replies_text = "\n\n".join([f"\ud83d\udcac {i+1}. {r}" for i, r in enumerate(suggested_replies)])

        return (
            f"\ud83d\udce9 *Nouveau DM de @{username}*\n\n"
            f"Message re\u00e7u :\n_{incoming_message}_\n\n"
            f"R\u00e9ponse sugg\u00e9r\u00e9e :\n{replies_text}\n\n"
            f"\ud83d\udc47 *Que veux-tu faire ?*"
        )

    def format_auto_notification(self, username, incoming_message, sent_replies):
        replies_text = "\n".join([f"  \u2192 {r}" for r in sent_replies])

        return (
            f"\ud83e\udd16 *[AUTO] R\u00e9ponse envoy\u00e9e \u00e0 @{username}*\n\n"
            f"Message re\u00e7u :\n_{incoming_message}_\n\n"
            f"R\u00e9ponses envoy\u00e9es :\n{replies_text}"
        )

    def build_approval_keyboard(self, sender_id, message_id):
        return {
            "inline_keyboard": [
                [
                    {"text": "\u2705 APPROUVER", "callback_data": f"approve:{sender_id}:{message_id}"},
                    {"text": "\u274c REJETER", "callback_data": f"reject:{sender_id}:{message_id}"}
                ],
                [
                    {"text": "\u270f\ufe0f MODIFIER", "callback_data": f"edit:{sender_id}:{message_id}"}
                ]
            ]
        }

    def parse_callback(self, callback_data):
        parts = callback_data.split(":")
        return {
            "action": parts[0],
            "sender_id": parts[1] if len(parts) > 1 else None,
            "message_id": parts[2] if len(parts) > 2 else None
        }
