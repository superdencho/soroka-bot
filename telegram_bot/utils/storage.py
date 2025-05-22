from models.message import Message


class AdminChatIDs:
    values = []


admin_chat_ids = AdminChatIDs()

# Список для хранения всех сообщений
chat_messages: list[Message] = []
