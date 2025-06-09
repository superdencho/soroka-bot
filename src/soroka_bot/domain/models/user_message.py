from dataclasses import dataclass
from datetime import datetime
from domain.models.chat_info import ChatInfo


@dataclass(slots=True)
class UserMessage:
    dt: datetime
    user: str
    text: str
    chat: ChatInfo
