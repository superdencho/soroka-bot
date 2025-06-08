from __future__ import annotations
from dataclasses import dataclass
from datetime import time
# from typing import Optional

from domain.repositories.recipient_repo import RecipientRepository
from domain.repositories.message_repo   import MessageRepository

@dataclass
class BotContext:
    token:       str
    db_path:     str 
    report_time: time
    recipients:  RecipientRepository
    messages:    MessageRepository

