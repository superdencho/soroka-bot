from typing import Iterable, Protocol

from soroka_bot.domain.models.user_message import UserMessage


class UserMessagesRepository(Protocol):
    """
    Абстракция для накопления и чтения сообщений пользователей.
    """

    async def add_message(self, msg: UserMessage) -> bool:
        """
        Добавить сообщение в хранилище.
        Вернуть True, если сохранение прошло успешно.
        """
        ...

    async def get_all_messages(self) -> list[UserMessage]:
        """
        Вернуть все накопленные сообщения пользователей.
        """
        ...

    async def clear(self) -> int:
        """
        Очистить хранилище сообщений,
        вернуть число удаленных записей.
        """
        ...

    def __iter__(self) -> Iterable[UserMessage]:
        """
        Итератор по текущим сообщениям.
        """
        ...
