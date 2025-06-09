from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import DATABASE_URL


engine = create_async_engine(DATABASE_URL)

# фабрика сессий
async_session = async_sessionmaker(engine, expire_on_commit=False)


# Базовый класс для всех ORM-моделей
class Base(DeclarativeBase):
    pass
