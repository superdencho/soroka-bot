from __future__ import annotations

from telegram.ext import Job
from dataclasses import dataclass
from datetime import time as dt_time
from typing import Any, Final, Mapping, MutableMapping

from application.jobs.daily_report import send_daily_report
from config import TZ_INFO
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes

# Тип DI‑контейнера
Services = Mapping[str, Any]


# ──────────────────────────────────────────────────────────────────────
# Общие константы и типы
# ──────────────────────────────────────────────────────────────────────
Services = Mapping[str, Any]
ChatData = MutableMapping[str, Any]
HOUR_PATTERN: Final[str] = r"^set_hour_(?:[01]?\d|2[0-3])$"  # 00-23


@dataclass(slots=True)
class StartCommandHandler:  # noqa: D101 – подробности в модуле-докстринге
    services: Services
    DEFAULT_HOUR: Final[int] = 20  # 20:00 — 8 PM

    # ────────────────────────────── основной коллбэк /start ──
    async def __call__(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        /,  # noqa: D401
    ) -> None:
        """Точка входа для команды /start."""
        chat = update.effective_chat
        if chat is None:  # pragma: no cover – PTB гарантирует, но mypy требует
            return

        # Гарантируем наличие job-а (или создаём с дефолтным временем)
        await self._ensure_daily_job(chat.id, context)

        # Регистрируем служебные CallbackQuery-хендлеры однократно на всё приложение
        if not context.application.bot_data.get("time_handlers_registered", False):
            context.application.add_handler(
                CallbackQueryHandler(self._edit_time, pattern="^edit_time$"),
                group=1,
            )
            context.application.add_handler(
                CallbackQueryHandler(self._set_time, pattern=HOUR_PATTERN),
                group=1,
            )
            context.application.bot_data["time_handlers_registered"] = True

        # Формируем клавиатуру главного меню
        keyboard: list[list[InlineKeyboardButton]] = [
            [InlineKeyboardButton(text="Старт", callback_data="start_report")],
            [
                InlineKeyboardButton(
                    text="Редактировать получателей", callback_data="edit_recipients"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Редактировать время отчёта", callback_data="edit_time"
                )
            ],
        ]
        if update.message:  # mypy: Optional[Message]
            await update.message.reply_text(
                (
                    "Привет! Я собираю сообщения чата и раз в сутки присылаю сводку.\n"
                    "Выберите действие:"
                ),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
            )

    # ──────────────────────────── вспомогательные методы ──
    async def _ensure_daily_job(
        self,
        chat_id: int,
        context: ContextTypes.DEFAULT_TYPE,
        /,  # noqa: D401
    ) -> None:
        """Планирует ежедневную задачу, если она ещё не создана."""
        chat_data: ChatData = context.chat_data

        # Час отчёта, сохранённый в `chat_data`, либо значение по умолчанию
        hour: int = int(chat_data.get("report_hour", self.DEFAULT_HOUR))
        chat_data["report_hour"] = hour  # фиксируем ключ, если его ещё не было

        if "report_job" in chat_data:  # noqa: SIM102 – намерено читаемо
            return  # job уже существует

        chat_data["report_job"] = self._create_daily_job(hour, chat_id, context)

    def _create_daily_job(
        self,
        hour: int,
        chat_id: int,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> Job:
        """Фактически регистрирует `Job` в планировщике и возвращает его."""
        job: Job = context.job_queue.run_daily(
            callback=self._send_daily_report,  # type: ignore[arg-type]  – PTB ожидает Callable[..., Awaitable]
            time=dt_time(hour, 0, tzinfo=ZoneInfo(TZ_INFO)),
            chat_id=chat_id,
            name=f"daily_report_{chat_id}",
        )
        return job

    async def _send_daily_report(self, context: ContextTypes.DEFAULT_TYPE, /) -> None:  # noqa: D401
        """Передаёт управление в бизнес-логику отправки отчёта."""
        await send_daily_report(context, self.services)

    # ─────────────────────────── обработка inline-кнопок ──
    async def _edit_time(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, /
    ) -> None:
        """Показывает клавиатуру с выбором часа."""
        query = update.callback_query
        if query is None:  # pragma: no cover — для mypy
            return
        await query.answer()

        buttons: list[list[InlineKeyboardButton]] = []
        row: list[InlineKeyboardButton] = []
        for hour in range(24):
            row.append(
                InlineKeyboardButton(
                    text=f"{hour:02d}", callback_data=f"set_hour_{hour:02d}"
                )
            )
            if len(row) == 6:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)

        await query.edit_message_text(
            text="Выберите час (Europe/Berlin), когда будет приходить ежедневный отчёт:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        )

    async def _set_time(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, /
    ) -> None:
        """Сохраняет выбранный час и пересоздаёт ежедневный `Job`."""
        query = update.callback_query
        if (
            query is None or query.data is None
        ):  # pragma: no cover – библиотека защищает, но mypy требует
            return
        await query.answer()

        # Извлекаем число часов из callback-данных ('set_hour_17' → 17)
        hour: int = int(query.data.rsplit("_", maxsplit=1)[-1])

        chat = update.effective_chat
        if chat is None:  # pragma: no cover
            return
        chat_id: int = chat.id

        chat_data: ChatData = context.chat_data
        chat_data["report_hour"] = hour

        # Удаляем старый job, если он был
        old_job: Optional[Job] = chat_data.pop("report_job", None)
        if old_job is not None:
            old_job.schedule_removal()

        # Создаём новый job и сохраняем его
        chat_data["report_job"] = self._create_daily_job(hour, chat_id, context)

        await query.edit_message_text(
            text=f"✔️ Время отчёта установлено на {hour:02d}:00 Europe/Berlin.",
        )


# ───────────────────────────────────────── точка входа ──
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE, /) -> None:  # noqa: D401
    """Функция-обёртка для регистрации в `Application`."""
    services: Services = context.bot_data.get("services", {})  # type: ignore[arg-type]
    await StartCommandHandler(services)(update, context)
