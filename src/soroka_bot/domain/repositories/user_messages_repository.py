from typing import Protocol

from soroka_bot.domain.models.user_message import UserMessage


class UserMessagesRepository(Protocol):
    """
    Абстракция для накопления и чтения сообщений пользователей.
    """

    async def add_message(self, msg: UserMessage) -> None:
        """
        Добавить сообщение в хранилище.
        """
        ...

    async def get_all_messages(self) -> list[UserMessage]:
        """
        Вернуть все накопленные сообщения пользователей.
        """
        ...

    async def clear_all_messages(self) -> int:
        """
        Очистить хранилище сообщений,
        вернуть число удаленных записей.
        """
        ...
