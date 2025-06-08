from __future__ import annotations
from dataclasses import dataclass
from datetime import time

from domain.repositories.recipients_repository import RecipientsRepository
from domain.repositories.user_messages_repository import UserMessagesRepository


@dataclass
class BotContext:
    token: str
    db_path: str
    report_time: time
    recipients: RecipientsRepository
    messages: UserMessagesRepository
