# handlers/start.py
import logging
from telegram import Update
from telegram.ext import ContextTypes
# from config import ADMIN_USERNAME
from config import ADMIN_USERNAMES
from utils.storage import admin_chat_ids

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username in ADMIN_USERNAMES:
        if update.effective_chat.id not in admin_chat_ids.values:
            admin_chat_ids.values.append(update.effective_chat.id)
        logger.info(f"Admin identified. Chat IDs: {admin_chat_ids.values}")
        await update.message.reply_text("Вы определены как администратор. Бот запущен, собираю сообщения!")
    else:
        await update.message.reply_text("Бот запущен. Сообщения собираются, но вы не админ.")
