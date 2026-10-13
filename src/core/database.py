from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing_extensions import AsyncGenerator
from src.core.settings import settings

DATABASE_URL = "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(
    settings.POSTGRES_DB_USER, settings.POSTGRES_DB_PASSWORD,
    settings.POSTGRES_DB_HOST,settings.POSTGRES_DB_PORT,
    settings.POSTGRES_DB_NAME
)

engine = create_async_engine(
    DATABASE_URL,
    isolation_level="READ COMMITTED"
)

SessionMaker = async_sessionmaker(
    bind=engine,
    expire_on_commit = False
)

Base = declarative_base()

## Test create db and tables
async def create_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def create_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionMaker() as session:
        try:
            yield session
        finally:
            await session.close()