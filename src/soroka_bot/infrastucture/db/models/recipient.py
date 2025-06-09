from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime


class Base(DeclarativeBase):
    pass


class DBRecipient(Base):
    __tablename__ = "recipients"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    user_name: Mapped[str] = mapped_column(String, nullable=False)
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
