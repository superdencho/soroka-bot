import logging
import openai
from rag_storage import read_rag_query

from config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_API_BASE,
    DEEPSEEK_MODEL,
    DEEPSEEK_TEMPERATURE,
)


logger = logging.getLogger(__name__)


def build_messages_for_deepseek(chat_messages: dict) -> list:
    """
    Генерируем массив сообщений в формате OpenAI ChatCompletion:
    [
      {"role": "system", "content": "..."},
      {"role": "user", "content": "..."},
      ...
    ]
    """
    rag_query = read_rag_query()
    system_content = (
        "You are a helpful assistant that processes Telegram chats. "
        "Follow the editorial rules given by the user. Summarize key events, conflicts, tasks, etc. "
        "Rewrite to simpler Russian if needed, according to the style rules. "
        "You are allowed to use emojis if appropriate to emphasize content or structure."
        "Use emojis for separation"
        "Do NOT use bold text (no double asterisks like **text**). "
        "Do NOT use dashed separators like '----'."
    )

    # Собираем всё содержимое чатов
    all_chats_text = []
    for cid, data in chat_messages.items():
        chat_title = data["chat_title"]
        for thread_id, thread_data in data["threads"].items():
            all_chats_text.append(f"Чат: {chat_title}; Тема: {thread_id}")
            for msg in thread_data["messages"]:
                dt = msg["datetime"]
                user = msg["user"]
                text = msg["text"]
                all_chats_text.append(f"{dt} — {user}: {text}")
            all_chats_text.append("")
    user_content = "\n".join(all_chats_text).strip()

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": f"{rag_query}\n\n{user_content}"},
        # ()) + user_content}
    ]
    return messages


def call_deepseek_openai(messages: list) -> str:
    """
    Вызывает DeepSeek через OpenAI API (совместимый интерфейс).
    """
    # Настраиваем openai на использование DeepSeek
    openai.api_key = DEEPSEEK_API_KEY
    openai.api_base = DEEPSEEK_API_BASE

    try:
        response = openai.ChatCompletion.create(
            model=DEEPSEEK_MODEL, messages=messages, temperature=DEEPSEEK_TEMPERATURE
        )
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        logger.error(f"DeepSeek request failed: {e}")
        return "Произошла ошибка при обращении к DeepSeek API."
