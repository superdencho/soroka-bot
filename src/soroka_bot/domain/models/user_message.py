from dataclasses import dataclass
from domain.models.chat_info import ChatInfo


@dataclass(slots=True)
class UserMessage:
    dt: str
    user: str
    text: str
    chat: ChatInfo
