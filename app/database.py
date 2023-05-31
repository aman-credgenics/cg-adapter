from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app import config
from app.logging import AppLogger

global_settings = config.get_settings()
logger = AppLogger.__call__().get_logger()

engine = create_async_engine(
    global_settings.asyncpg_url,
    future=True,
    echo=True,
)

# expire_on_commit=False will prevent attributes from being expired
# after commit.
AsyncSessionFactory = sessionmaker(engine, autoflush=False, expire_on_commit=False, class_=AsyncSession)


# Dependency
async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        logger.debug(f"ASYNC Pool: {engine.pool.status()}")
        yield session


