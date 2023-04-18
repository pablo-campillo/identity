from typing import List
from pydantic.error_wrappers import ValidationError

from identity.domain.users import User
from identity.domain.pagination import Page
from identity.services.security import get_password_hash
from identity.services.uow.users import UsersAbstractUnitOfWork


class UserAlreadyExists(Exception):
    pass


class UserDoesNotExist(Exception):
    pass


class InvalidEmailFormat(Exception):
    pass


async def new_user(email: str, plain_password: str, uow: UsersAbstractUnitOfWork) -> User:
    try:
        hashed_password = get_password_hash(plain_password)
        new_user_param = User(email=email, password=hashed_password)
    except ValidationError as ve:
        raise InvalidEmailFormat()

    async with uow:
        if await uow.users.get_user(email) is not None:
            raise UserAlreadyExists()

        new_user = await uow.users.add_user(new_user_param)
        await uow.commit()
    return new_user


async def get_user(email: str, uow: UsersAbstractUnitOfWork) -> User:
    async with uow:
        user = await uow.users.get_user(email)
        if user is None:
            raise UserDoesNotExist()
        return user


async def list_users(uow: UsersAbstractUnitOfWork) -> List[User]:
    async with uow:
        return await uow.users.list_users()


async def list_paginated_users(uow: UsersAbstractUnitOfWork, page:int = 1, page_size:int = 100_000) -> Page[User]:
    async with uow:
        return await uow.users.list_paginated_users(page, page_size)
    

async def validate_user(email: str, uow: UsersAbstractUnitOfWork) -> User:
    async with uow:
        user = await uow.users.get_user(email)
        if user is None:
            raise UserDoesNotExist()
        user.validate()
        user = await uow.users.update_user(user)
        await uow.commit()
        return user


async def disable_user(email: str, uow: UsersAbstractUnitOfWork) -> User:
    async with uow:
        user = await uow.users.get_user(email)
        if user is None:
            raise UserDoesNotExist()
        user.disable()
        user = await uow.users.update_user(user)
        await uow.commit()
        return user


async def enable_user(email: str, uow: UsersAbstractUnitOfWork) -> User:
    async with uow:
        user = await uow.users.get_user(email)
        if user is None:
            raise UserDoesNotExist()
        user.enable()
        user = await uow.users.update_user(user)
        await uow.commit()
        return user
