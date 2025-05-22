from dataclasses import dataclass


@dataclass(slots=True)
class Message:
    dt: str
    user: str
    text: str
    chat_id: int
    chat_title: str
    thread_id: int
