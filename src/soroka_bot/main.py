import logging
import threading
# from datetime import time
# from zoneinfo import ZoneInfo

from telegram.ext import ApplicationBuilder, CommandHandler

from config import TELEGRAM_BOT_TOKEN, DAILY_JOB_HOUR, DAILY_JOB_MINUTE, TZ_INFO
from infrastucture.db.base import async_session
from infrastucture.db.repositories.user_messages_repository import (
    SqlAlchemyUserMessagesRepository,
)
from infrastucture.db.repositories.recipients_repository import (
    SqlAlchemyRecipientsRespository,
)

from application.handlers.start import start_command
# from .application.handlers.collector import collect_messages
# TODO: импортировать хендлеры для управления списком получателей (add, list, clear)
# from .application.jobs.daily_report import send_daily_report

logger = logging.getLogger(__name__)


def run_bot() -> None:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    # Инициализация репозиториев
    message_repo = SqlAlchemyUserMessagesRepository(async_session)
    recipient_repo = SqlAlchemyRecipientsRespository(async_session)
    services = {
        "message_repo": message_repo,
        "recipient_repo": recipient_repo,
    }

    # Создание и настройка бота
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.bot_data["report_hours"] = {}

    # Регистрация хендлеров
    application.add_handler(CommandHandler("start", start_command))
    # application.add_handler(Comm)
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, collect_messages))
    # TODO: добавить CommandHandler/ConversationHandler для add_recipients, list_recipients, clear_recipients

    # Планирование ежедневной отправки отчёта
    # job_queue = application.job_queue
    # job_queue.run_daily(
    #     send_daily_report,
    #     time=time(DAILY_JOB_HOUR, DAILY_JOB_MINUTE, tzinfo=ZoneInfo(TZ_INFO)),
    #     days=tuple(range(7)),
    # )
    logger.info(
        f"Scheduled daily report at {DAILY_JOB_HOUR:02d}:{DAILY_JOB_MINUTE:02d} {TZ_INFO}"
    )

    # Запуск polling
    logger.info("Starting Telegram bot polling...")
    application.run_polling()


if __name__ == "__main__":
    # Запуск бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    # Держим основной поток живым
    bot_thread.join()
