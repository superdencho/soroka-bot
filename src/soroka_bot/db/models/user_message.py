from datetime import datetime, timezone

from db.base import Base
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class DBUserMessage(Base):
    __tablename__ = "messages"

    # PRIMARY KEY с авто-инкрементом (для SQLite это значение по умолчанию)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_name: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    chat_id: Mapped[int] = mapped_column(Integer, nullable=False)
    chat_title: Mapped[str | None] = mapped_column(String, nullable=True)

    # ID потока (topic/thread) внутри чата тоже может не быть
    thread_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Время получения/сохранения сообщения
    dt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
