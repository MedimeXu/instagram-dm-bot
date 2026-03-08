import json
import threading
from flask import Flask, request, jsonify
from app.config import Config
from app.database import ConversationDB
from app.instagram import InstagramClient
from app.claude_client import ClaudeClient
from app.telegram_bot import TelegramValidator
from app.prompts import build_system_prompt, build_user_message


pending_replies = {}


def process_incoming_dm(sender_id, text, message_id, ig_client, db, claude, telegram, config):
    profile = ig_client.get_user_profile(sender_id)
    username = profile.get("username", "inconnu")
    name = profile.get("name", "Inconnu")

    db.save_user_info(sender_id, name, username)
    db.save_message(sender_id, "incoming", text)

    history = db.get_conversation(sender_id)
    system_prompt = build_system_prompt()
    user_message = build_user_message(history[:-1], text, username)

    response = claude.generate_response(system_prompt, user_message)
    bubbles = claude.parse_bubbles(response)

    if config.AUTO_MODE:
        ig_client.send_multiple_messages(sender_id, bubbles)
        for bubble in bubbles:
            db.save_message(sender_id, "outgoing", bubble)
    else:
        pending_replies[f"{sender_id}:{message_id}"] = {
            "sender_id": sender_id,
            "username": username,
            "bubbles": bubbles,
            "original_message": text
        }


def create_app(testing=False):
    app = Flask(__name__)

    if testing:
        config = Config()
        config.META_VERIFY_TOKEN = "test_verify"
    else:
        config = Config()

    app.config["APP_CONFIG"] = config

    @app.route("/webhook", methods=["GET"])
    def verify_webhook():
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == config.META_VERIFY_TOKEN:
            return challenge, 200
        return "Forbidden", 403

    @app.route("/webhook", methods=["POST"])
    def receive_webhook():
        payload = request.get_json()

        if payload.get("object") != "instagram":
            return "Not found", 404

        ig_client = InstagramClient(
            config.META_PAGE_ACCESS_TOKEN,
            config.META_APP_SECRET,
            config.INSTAGRAM_ACCOUNT_ID
        )

        messages = ig_client.parse_webhook(payload)

        for msg in messages:
            if msg["sender_id"] == config.INSTAGRAM_ACCOUNT_ID:
                continue

            thread = threading.Thread(
                target=process_incoming_dm,
                args=(
                    msg["sender_id"],
                    msg["text"],
                    msg.get("message_id", ""),
                    ig_client,
                    ConversationDB(config.DATABASE_PATH),
                    ClaudeClient(mode=config.CLAUDE_MODE, api_key=config.ANTHROPIC_API_KEY),
                    TelegramValidator(config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_ADMIN_CHAT_ID),
                    config
                )
            )
            thread.start()

        return "OK", 200

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "ok",
            "auto_mode": config.AUTO_MODE
        })

    @app.route("/auto-mode/toggle", methods=["POST"])
    def toggle_auto():
        config.toggle_auto_mode()
        return jsonify({
            "auto_mode": config.AUTO_MODE,
            "message": f"Mode auto {'activ\u00e9' if config.AUTO_MODE else 'd\u00e9sactiv\u00e9'}"
        })

    return app
