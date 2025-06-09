# import logging
# import openai
# from importlib.resources import files
# from models.deepseek_message import DeepSeekMessage, DeepSeekRole 
#
# from config import (
#     DEEPSEEK_API_KEY,
#     DEEPSEEK_API_BASE,
#     DEEPSEEK_MODEL,
#     DEEPSEEK_TEMPERATURE,
# )
#
#
# logger = logging.getLogger(__name__)
#
# _resource_pkg = "soroka_bot.shared"  # пакет-контейнер
# RAG_QUERY: str = (files(_resource_pkg) / "rag.txt").read_text(encoding="utf-8")
# SYSTEM_CONTENT: str = (files(_resource_pkg) / "ai_system_message.txt").read_text(
#     encoding="utf-8"
# )
#
#
# def build_messages_for_deepseek(chat_messages: dict[str, str]) -> list[DeepSeekMessage]:
#     """
#     Генерируем массив сообщений в формате DeepSeek ChatCompletion:
#     [
#       {"role": "system", "content": "..."},
#       {"role": "user", "content": "..."},
#       ...
#     ]
#     """
#
#     # Собираем всё содержимое чатов
#     all_chats_text = []
#     for cid, data in chat_messages.items():
#         chat_title = data["chat_title"]
#         for thread_id, thread_data in data["threads"].items():
#             all_chats_text.append(f"Чат: {chat_title}; Тема: {thread_id}")
#             for msg in thread_data["messages"]:
#                 dt = msg["datetime"]
#                 user = msg["user"]
#                 text = msg["text"]
#                 all_chats_text.append(f"{dt} — {user}: {text}")
#             all_chats_text.append("")
#     user_content = "\n".join(all_chats_text).strip()
#
#     messages = [
#         DeepSeekMessage(role=DeepSeekRole.system, content=SYSTEM_CONTENT),
#         DeepSeekMessage(
#             role=DeepSeekRole.user, content=f"{RAG_QUERY}\n\n{user_content}"
#         ),
#     ]
#     return messages
#
#
# def call_deepseek_openai(messages: list[DeepSeekMessage]) -> str:
#     """
#     Вызывает DeepSeek через DeepSeek API.
#     """
#     # Настраиваем openai на использование DeepSeek
#     openai.api_key = DEEPSEEK_API_KEY
#     openai.api_base = DEEPSEEK_API_BASE
#
#     try:
#         response = openai.ChatCompletion.create(
#             model=DEEPSEEK_MODEL, messages=messages, temperature=DEEPSEEK_TEMPERATURE
#         )
#         answer = response.choices[0].message.content
#         return answer
#     except Exception as e:
#         logger.error(f"DeepSeek request failed: {e}")
#         return "Произошла ошибка при обращении к DeepSeek API."
