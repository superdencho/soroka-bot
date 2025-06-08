from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer
from infrastructure.sqlite.base import Base


class RecipientModel(Base):
    __tablename__ = "recipients"
    name = Column(String, nullable=False)
    user_id = Column(Integer, primary_key=True, unique=True)
    Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
