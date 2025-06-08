from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class ChatInfo:
    chat_id: int
    chat_title: Optional[str] = None
    thread_id: Optional[int] = None
