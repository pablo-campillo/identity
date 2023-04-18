import pytest

from identity.services.uow.users import UsersSqlAlchemyUnitOfWork
from identity.services.users import new_user, get_user, UserDoesNotExist

@pytest.mark.asyncio
async def test_get_user_service(session_maker):
    uow = UsersSqlAlchemyUnitOfWork(session_maker)

    email = 'petete@version1.com'
    pw = 'mypw'
    await new_user(email, pw, uow)

    user = await get_user(email, uow)

    assert user.email == email
    assert user.password != pw
    assert not user.active
    assert not user.validated


@pytest.mark.asyncio
async def test_get_user_service_user_does_not_exist_exception(session_maker):
    uow = UsersSqlAlchemyUnitOfWork(session_maker)

    email = 'petete@version1.com'
    pw = 'mypw'

    with pytest.raises(UserDoesNotExist):
        await get_user(email, uow)
