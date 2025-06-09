import os
from typing import Final

from dotenv import load_dotenv


load_dotenv()

try:
    TELEGRAM_BOT_TOKEN: Final[str] = os.environ["TELEGRAM_BOT_TOKEN"]
except KeyError as exc:
    raise RuntimeError(
        "Переменная окружения TELEGRAM_BOT_TOKEN не установлена."
    ) from exc

TZ_INFO = "Europe/Moscow"
DATABASE_URL = "sqlite+aiosqlite:///soroka_bot.db"

# TODO: это нужно перенести в функционал UI
# Время (часы и минуты) для ежедневной задачи.
DAILY_JOB_HOUR = 19
DAILY_JOB_MINUTE = 11

# Параметры DeepSeek
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_BASE = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-reasoner"
DEEPSEEK_TEMPERATURE: float = 1.0
