# utils/formatting.py
# from typing import List
#
# def format_weekly_report(chat_messages: dict) -> str:
#     """
#     Формируем единый текст с разбивкой по чатам и темам.
#     """
#     lines = []
#     for cid, data in chat_messages.items():
#         chat_title = data["chat_title"]
#         for thread_id, thread_data in data["threads"].items():
#             lines.append(f"📢 Беседа: {chat_title}; Тема: {thread_data['thread_id']}")
#             for msg in thread_data["messages"]:
#                 dt = msg["datetime"]
#                 user = msg["user"]
#                 text = msg["text"]
#                 lines.append(f"🕒 {dt} — {user}: {text}")
#             lines.append("")  # Пустая строка-разделитель
#     return "\n".join(lines).strip()
#
# def chunk_text(text: str, max_size: int = 4000) -> List[str]:
#     """
#     Делим текст на порции, чтобы не превышать лимит Telegram (≈4096).
#     """
#     return [text[i:i+max_size] for i in range(0, len(text), max_size)]
