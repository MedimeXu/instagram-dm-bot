import asyncio
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from app.config import config
from app.telegram_bot import TelegramValidator
from app.instagram import InstagramClient
from app.database import ConversationDB
from app.webhook import pending_replies

logger = logging.getLogger(__name__)

validator = TelegramValidator(config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_ADMIN_CHAT_ID)
ig_client = InstagramClient(config.META_PAGE_ACCESS_TOKEN, config.META_APP_SECRET, config.INSTAGRAM_ACCOUNT_ID)
db = ConversationDB(config.DATABASE_PATH)

editing_state = {}


async def start(update: Update, context):
    await update.message.reply_text(
        "\ud83e\udd16 Bot DM Juliette actif !\n\n"
        "Commandes :\n"
        "/status \u2014 \u00c9tat du bot\n"
        "/auto \u2014 Activer/d\u00e9sactiver le mode auto\n"
    )


async def status(update: Update, context):
    mode = "\ud83d\udfe2 AUTO" if config.AUTO_MODE else "\ud83d\udfe1 SEMI-AUTO (validation)"
    count = len(pending_replies)
    await update.message.reply_text(
        f"\ud83d\udcca *Status*\n\n"
        f"Mode : {mode}\n"
        f"DM en attente : {count}",
        parse_mode="Markdown"
    )


async def toggle_auto(update: Update, context):
    config.toggle_auto_mode()
    mode = "\ud83d\udfe2 AUTO" if config.AUTO_MODE else "\ud83d\udfe1 SEMI-AUTO"
    await update.message.reply_text(f"Mode chang\u00e9 \u2192 {mode}")


async def handle_callback(update: Update, context):
    query = update.callback_query
    await query.answer()

    data = validator.parse_callback(query.data)
    key = f"{data['sender_id']}:{data['message_id']}"

    if key not in pending_replies:
        await query.edit_message_text("\u26a0\ufe0f Ce message a d\u00e9j\u00e0 \u00e9t\u00e9 trait\u00e9.")
        return

    pending = pending_replies[key]

    if data["action"] == "approve":
        ig_client.send_multiple_messages(pending["sender_id"], pending["bubbles"])
        for bubble in pending["bubbles"]:
            db.save_message(pending["sender_id"], "outgoing", bubble)
        await query.edit_message_text(f"\u2705 R\u00e9ponse envoy\u00e9e \u00e0 @{pending['username']}")
        del pending_replies[key]

    elif data["action"] == "reject":
        await query.edit_message_text(f"\u274c R\u00e9ponse rejet\u00e9e pour @{pending['username']}")
        del pending_replies[key]

    elif data["action"] == "edit":
        editing_state[str(query.from_user.id)] = key
        await query.edit_message_text(
            f"\u270f\ufe0f Envoie ta r\u00e9ponse modifi\u00e9e pour @{pending['username']}\n"
            f"(S\u00e9pare les bulles avec ---)\n\n"
            f"Message original : _{pending['original_message']}_",
            parse_mode="Markdown"
        )


async def handle_edit_reply(update: Update, context):
    user_id = str(update.message.from_user.id)

    if user_id not in editing_state:
        return

    key = editing_state[user_id]
    if key not in pending_replies:
        await update.message.reply_text("\u26a0\ufe0f Ce message a d\u00e9j\u00e0 \u00e9t\u00e9 trait\u00e9.")
        del editing_state[user_id]
        return

    pending = pending_replies[key]
    new_bubbles = [b.strip() for b in update.message.text.split("---") if b.strip()]

    ig_client.send_multiple_messages(pending["sender_id"], new_bubbles)
    for bubble in new_bubbles:
        db.save_message(pending["sender_id"], "outgoing", bubble)

    await update.message.reply_text(f"\u2705 R\u00e9ponse modifi\u00e9e envoy\u00e9e \u00e0 @{pending['username']}")

    del pending_replies[key]
    del editing_state[user_id]


def run_telegram_bot():
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("auto", toggle_auto))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_edit_reply))

    logger.info("Telegram bot started")
    app.run_polling()
