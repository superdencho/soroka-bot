from typing import Protocol
from domain.models.recipient import Recipient


class RecipientsRepository(Protocol):
    """
    Абстракция для хранения списка получателей отчета.
    """

    async def add_recipients(self, recipients: list[Recipient]) -> set[str]:
        """
        Добавить одного или нескольких получателей (username без @),
        вернуть набор добавленных имен.
        """
        ...

    async def get_current_recipients(self) -> list[str]:
        """
        Вернуть список текущих пользователей.
        """
        ...

    async def clear_recipient_list(self) -> int:
        """
        Очистить список всех получателей,
        вернуть количество удаленных записей.
        """
        ...
