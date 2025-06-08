import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

from models.message import Message
from utils.storage import chat_messages

logger = logging.getLogger(__name__)


async def collect_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is None or update.effective_message is None:
        return

    tg_message = update.effective_message
    chat_id: int = update.effective_chat.id
    dt: str = datetime.now().strftime("%Y-%m-%d %H:%M")
    thread_id: int = tg_message.message_thread_id if tg_message.message_thread_id else 0
    chat_title: str = update.effective_chat.title or "Личная переписка/неизвестный чат"

    if tg_message.from_user:
        user = tg_message.from_user
        parts: list[str] = []
        if user.first_name:
            parts.append(user.first_name)
        if user.last_name:
            parts.append(user.last_name)
        if user.username:
            parts.append(f"(@{user.username})")
        user_name: str = " ".join(parts)
    else:
        user_name = "Неизвестный пользователь"

    # Проверяем, не документ ли это
    text: str = tg_message.text or ""
    if tg_message.document:
        doc_name = tg_message.document.file_name
        text = f"Файл: {doc_name}"

    logger.info(f"Собрано сообщение от {user_name.strip()} в чате {chat_title}: {text}")

    chat = chat_messages.setdefault(
        chat_id, ChatModel(chat_id=chat_id, chat_title=chat_title, threads={})
    )
    thread = chat.threads.setdefault(thread_id, ThreadModel(thread_id=thread_id))
    message = MessageModel(dt=dt, user=user_name.strip(), text=text)
    thread.add_message(message)
