import threading
import logging
from app.webhook import create_app
from app.telegram_runner import run_telegram_bot
from app.config import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting Instagram DM Bot for Juliette WMA")
    logger.info(f"Mode: {'AUTO' if config.AUTO_MODE else 'SEMI-AUTO'}")

    # Start Telegram bot in a separate thread
    telegram_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    telegram_thread.start()
    logger.info("Telegram bot started")

    # Start Flask webhook server
    app = create_app()
    logger.info(f"Flask server starting on port {config.FLASK_PORT}")
    app.run(host="0.0.0.0", port=config.FLASK_PORT)


if __name__ == "__main__":
    main()
