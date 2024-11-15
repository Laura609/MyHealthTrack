from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Создание базового класса для моделей
Base = declarative_base()

# Указание строки подключения (замените на вашу строку подключения)
DATABASE_URL = "postgresql+asyncpg://username:password@localhost/dbname"  # Например, для PostgreSQL

# Создаем асинхронный движок базы данных
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем фабрику для сессий
Session = sessionmaker(
    engine,
    class_=AsyncSession,  # Указываем, что сессия будет асинхронной
    expire_on_commit=False,  # Отключаем автообновление после коммита
)
