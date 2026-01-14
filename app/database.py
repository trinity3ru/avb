import os
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

# 1. Настройка URL из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///urls.db")

# 2. Создание движка
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 3. Создание фабрики сессий
new_session = async_sessionmaker(engine, expire_on_commit=False)


# 4. Базовый класс для моделей
# MappedAsDataclass - нужен для удобной работы с типами (новинка 2.0)
class Model(MappedAsDataclass, DeclarativeBase):
    pass


async def get_db():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]
