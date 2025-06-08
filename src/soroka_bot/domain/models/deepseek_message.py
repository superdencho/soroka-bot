from dataclasses import dataclass
from enum import Enum


class DeepSeekRole(Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


@dataclass(slots=True)
class DeepSeekMessage:
    role: DeepSeekRole
    content: str
