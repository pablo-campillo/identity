from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from identity.config import get_database_url

engine = create_async_engine(
    get_database_url(),
    # echo=settings.DB_ECHO_LOG,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)
