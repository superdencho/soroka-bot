import logging

from db.base import async_session, async_sessionmaker
from db.models.recipient import DBRecipient
from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.recipient import Recipient
from domain.repositories.recipients_repository import RecipientsRepository
from domain.models.errors import RecipientSaveError

logger = logging.getLogger(__name__)


class SqlAlchemyRecipientsRespository(RecipientsRepository):
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession] = async_session,
    ) -> None:
        self._session_factory = session_factory

    async def add_recipients(self, recipients: list[Recipient]) -> set[str]:
        added_names: set[str] = set()
        if not recipients:
            return added_names

        unique: dict[int, Recipient] = {r.user_id: r for r in recipients}

        try:
            async with self._session_factory() as session, session.begin():
                # существующие записи
                rows = (
                    (
                        await session.execute(
                            select(DBRecipient).where(
                                DBRecipient.user_id.in_(unique.keys())
                            )
                        )
                    )
                    .scalars()
                    .all()
                )
                existing_by_id: dict[int, DBRecipient] = {r.user_id: r for r in rows}

                for uid, rec in unique.items():
                    # обновляем имена пользователей, если они изменились
                    db_obj = existing_by_id.get(uid)
                    if db_obj:
                        if db_obj.user_name != rec.username:
                            db_obj.user_name = rec.username

                    else:
                        session.add(
                            DBRecipient(
                                user_id=rec.user_id,
                                user_name=rec.username,
                                added_at=rec.added_at,
                            )
                        )
                        added_names.add(rec.username)

            logger.info(
                "получатели сохранены",
                extra={
                    "user_ids": list(unique.keys()),
                    "added": list(added_names),
                },
            )
            return added_names

        except SQLAlchemyError as exc:
            logger.exception(
                "recipients_save_failed",
                extra={"user_ids": list(unique.keys()), "err": str(exc)},
            )
            raise RecipientSaveError from exc

    async def get_current_recipients(self) -> list[str]:
        async with self._session_factory() as session:
            result = await session.execute(select(DBRecipient.user_name))
            return sorted(result.scalars().all())

    async def clear_recipient_list(self) -> int:
        async with self._session_factory() as session, session.begin():
            res = await session.execute(delete(DBRecipient))
            return res.rowcount or 0
