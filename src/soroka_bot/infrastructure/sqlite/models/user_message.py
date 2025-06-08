from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from infrastructure.sqlite.base import Base

class MessageModel(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String, nullable=False)
    text = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=False)
    chat_title = Column(String, nullable=True)
    thread_id = Column(Integer, nullable=True)
    dt = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
