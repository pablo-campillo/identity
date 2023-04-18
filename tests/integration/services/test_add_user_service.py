import pytest

from identity.services.uow.users import UsersSqlAlchemyUnitOfWork
from identity.services.users import new_user, UserAlreadyExists, InvalidEmailFormat

@pytest.mark.asyncio
async def test_add_user_service(session_maker):
    uow = UsersSqlAlchemyUnitOfWork(session_maker)

    email = 'petete@version1.com'
    pw = 'mypw'
    user = await new_user(email, pw, uow)

    assert user.email == email
    assert user.password != pw
    assert not user.active
    assert not user.validated


@pytest.mark.asyncio
async def test_add_user_service_user_already_exist_exception(session_maker):
    uow = UsersSqlAlchemyUnitOfWork(session_maker)

    email = 'petete@version1.com'
    pw = 'mypw'
    user = await new_user(email, pw, uow)

    with pytest.raises(UserAlreadyExists):
        await new_user(email, pw, uow)


@pytest.mark.asyncio
async def test_add_user_service_invalid_email(session_maker):
    uow = UsersSqlAlchemyUnitOfWork(session_maker)

    email = 'petete'
    pw = 'mypw'
    with pytest.raises(InvalidEmailFormat):
        user = await new_user(email, pw, uow)
