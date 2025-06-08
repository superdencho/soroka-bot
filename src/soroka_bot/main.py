import logging
import threading
from datetime import time
from zoneinfo import ZoneInfo

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from telegram_bot.handlers.collector import collect_messages
from telegram_bot.handlers.start import start_command
from telegram_bot.jobs.daily_report import send_daily_report

from .config import DAILY_JOB_HOUR, DAILY_JOB_MINUTE, TOKEN, TZ_INFO

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.ALL, collect_messages))

    job_queue = application.job_queue
    job_queue.run_daily(
        send_daily_report,
        time=time(DAILY_JOB_HOUR, DAILY_JOB_MINUTE, tzinfo=ZoneInfo(TZ_INFO)),
        days=tuple(range(7)),
    )
    logger.info(
        f"Scheduled daily report at {DAILY_JOB_HOUR}:{DAILY_JOB_MINUTE} {TZ_INFO}"
    )

    logger.info("Starting Telegram bot polling...")
    application.run_polling()


if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
