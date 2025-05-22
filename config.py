import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN is not set. Please export it as an environment variable."
    )

ADMIN_USERNAMES = ["denis_varekha", "igor_gerasimov"]
TZ_INFO = "Europe/Moscow"

BASE_DIR    = Path(__file__).parent
SHARED_DIR  = BASE_DIR / "shared"

RAG_FILE    = SHARED_DIR / "rag.txt"
DEFAULT_RAG = """Собери из этого ключевые события для отчёта... [ваш текущий текст]..."""

# Время (часы и минуты) для ежедневной задачи.
DAILY_JOB_HOUR = 19
DAILY_JOB_MINUTE = 11

# Параметры DeepSeek
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_BASE = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-reasoner"
DEEPSEEK_TEMPERATURE: float = 1.0
