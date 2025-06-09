import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select, delete

from db.base import async_session
from db.models.user_message import DBUserMessage
from domain.repositories.user_messages_repository import UserMessagesRepository
from domain.models.user_message import UserMessage, ChatInfo
from domain.models.errors import MessageSaveError

logger = logging.getLogger(__name__)


class SqlAlchemyUserMessagesRepository(UserMessagesRepository):
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession] = async_session,
    ) -> None:
        self._session_factory = session_factory

    async def add_message(self, msg: UserMessage) -> None:
        try:
            async with self._session_factory() as session, session.begin():
                session.add(
                    DBUserMessage(
                        user_name=msg.user,
                        text=msg.text,
                        chat_id=msg.chat.chat_id,
                        chat_title=msg.chat.chat_title,
                        thread_id=msg.chat.thread_id,
                        dt=msg.dt,
                    )
                )
            logger.info("Сообщение от пользователя %s сохранено", msg.user)
        except SQLAlchemyError as exc:
            logger.exception("Не удалось сохранить сообщение: %s", exc)
            raise MessageSaveError from exc

    async def get_all_messages(self) -> list[UserMessage]:
        async with self._session_factory() as session:
            result = await session.execute(
                select(DBUserMessage).order_by(DBUserMessage.dt)
            )
            return [
                UserMessage(
                    dt=row.dt,
                    user=row.user_name,
                    text=row.text,
                    chat=ChatInfo(
                        chat_id=row.chat_id,
                        chat_title=row.chat_title,
                        thread_id=row.thread_id,
                    ),
                )
                for row in result.scalars()
            ]

    async def clear_all_messages(self) -> int:
        async with self._session_factory() as session, session.begin():
            res = await session.execute(delete(DBUserMessage))
            return res.rowcount or 0
