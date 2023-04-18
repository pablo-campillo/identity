import pytest

from identity.services.uow.users import UsersSqlAlchemyUnitOfWork
from identity.services.users import list_users, list_paginated_users

@pytest.mark.asyncio
async def test_empty_list_users_service(session_maker):
    uow = UsersSqlAlchemyUnitOfWork(session_maker)
    users = await list_users(uow)
    assert len(users) == 0


@pytest.mark.asyncio
async def test_list_users_service(init_database, session_maker):
    uow = UsersSqlAlchemyUnitOfWork(session_maker)
    users = await list_users(uow)
    assert len(users) == 3

@pytest.mark.asyncio
async def test_list_default_paginated_users(init_database, session_maker):
    uow = UsersSqlAlchemyUnitOfWork(session_maker)
    page = await list_paginated_users(uow)
    assert len(page.items) == 3
    assert page.page == 1
    assert page.page_size == 100_000
    assert page.total == 3
    assert not page.has_next

@pytest.mark.asyncio
async def test_list_paginated_users_page1_size1(init_database, session_maker):
    uow = UsersSqlAlchemyUnitOfWork(session_maker)
    page = await list_paginated_users(uow, page=1, page_size=1)
    assert len(page.items) == 1
    assert page.page == 1
    assert page.page_size == 1
    assert page.total == 3
    assert page.has_next

@pytest.mark.asyncio
async def test_list_paginated_users_page3_size1(init_database, session_maker):
    uow = UsersSqlAlchemyUnitOfWork(session_maker)
    page = await list_paginated_users(uow, page=3, page_size=1)
    assert len(page.items) == 1
    assert page.page == 3
    assert page.page_size == 1
    assert page.total == 3
    assert not page.has_next
