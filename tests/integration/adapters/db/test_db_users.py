import pytest
from datetime import datetime
from sqlalchemy.sql import text
from sqlalchemy import select

from identity.adapters.db.tables import users as db
from identity.domain.users import User

@pytest.mark.asyncio
async def test_new_user_and_domain_orm_mapping(session_maker):
    session = session_maker()
    user = None
    try:
        await session.execute(
            text("INSERT INTO users (created_at, updated_at, email, password, active, validated) VALUES "
            '("2004-05-23T14:25:10", "2004-05-23T14:25:10", "petete@version1.com", "mypass", false, false);')
        )
        d = datetime.fromisoformat("2004-05-23T14:25:10")
        expected = User(created_at=d, updated_at=d, email="petete@version1.com", password="mypass")
        db_user = await session.get(db.User, 'petete@version1.com')
        user = User.from_orm(db_user)
    except Exception as ex:
        print("EXCEPTION!!!")
        raise
    finally:
        await session.close()
    assert user == expected
