from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

from typing import Annotated

from fastapi import Depends
 

# 1. Настройка URL
# Файл tasks.db создастся в корне проекта
DATABASE_URL = "sqlite+aiosqlite:///urls.db"

# 2. Создание движка
engine = create_async_engine(DATABASE_URL)

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