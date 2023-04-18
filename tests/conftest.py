import asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.sql import text

from identity.adapters.db.tables import Base
# from identity.adapters.db.tables.users import User


async def init_models(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture
def in_memory_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    asyncio.run(init_models(engine))
    return engine


@pytest.fixture
def session_maker(in_memory_db):
    yield async_sessionmaker(bind=in_memory_db, expire_on_commit=False)


async def init_database_with_users(session_maker):
    session = session_maker()
    try:
        await session.execute(
            text("INSERT INTO users (created_at, updated_at, email, password, active, validated) VALUES "
            '("2023-04-01T10:00:00", "2023-04-01T10:00:00", "pepita@version1.com", "mypass1", false, false),'
            '("2023-04-02T11:00:00", "2023-04-03T11:00:00", "purita@version1.com", "mypass2", false, true),'
            '("2023-04-03T12:00:00", "2023-04-04T12:00:00", "potato@version1.com", "mypass2", true, true);'
            )
        )
        await session.commit()
    except Exception as ex:
        raise
    finally:
        await session.close()

@pytest.fixture
def init_database(session_maker):
    asyncio.run(init_database_with_users(session_maker))
