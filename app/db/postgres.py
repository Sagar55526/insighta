from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator
from app.core.config import settings

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_SERVER}:"
    f"{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DB}"
)

engine = create_async_engine(
    url = DATABASE_URL,
    echo = False,
    poolClass = NullPool,           # avoids connection issues in async tasks
)

AsyncSessionLocal = sessionmaker(
    engine = engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_postgres_session() ->  AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session