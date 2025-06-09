from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Recipient:
    user_id: int
    username: str
    added_at: datetime
