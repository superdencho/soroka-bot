import logging

# from application.templates
from telegram.ext import ContextTypes
# from utils.formatting import chunk_text

logger = logging.getLogger(__name__)


async def send_daily_report(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Отправка отчёта.
    Формирует запрос в ИИ-сервис, отправляет ответ, затем чистит БД сообщений.
    """
    # if admin_chat_ids.values is None:
    #     logger.error(
    #         "Admin chat ID not set. Cannot send report. Use /start with admin user."
    #     )
    #     return
    #
    # if not chat_messages:
    #     logger.info("No messages collected, sending empty report notification")
    #     try:
    #         for user_chat_id in admin_chat_ids.values:
    #             await context.bot.send_message(
    #                 chat_id=user_chat_id, text="На сегодня сообщений не собрано."
    #             )
    #
    #     except Exception as e:
    #         logger.error(f"Failed to send empty report: {e}")
    #     return
    #
    # # 1. Формируем массив сообщений в стиле RAG
    # messages = build_messages_for_deepseek(chat_messages)
    #
    # # 2. Запрашиваем DeepSeek (через openai API)
    # try:
    #     ai_response = call_deepseek_openai(messages)
    # except Exception as e:
    #     logger.error(f"Failed to get AI report: {e}")
    #     ai_response = "Произошла ошибка при обращении к DeepSeek AI."
    #
    # # 3. Отправляем ответ бота (дробим при необходимости)
    # for user_chat_id in admin_chat_ids.values:
    #     for part in chunk_text(ai_response):
    #         await context.bot.send_message(
    #             chat_id=user_chat_id,
    #             text=part,
    #         )
    #
    # # 4. После отправки — очищаем словарь, чтобы начать новый день/неделю с чистой историей
    # chat_messages.clear()
    # logger.info("Daily AI-based report successfully sent to admin")
