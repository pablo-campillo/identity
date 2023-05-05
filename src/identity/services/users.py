"""Module that contains all functions for managing users.

.. note::
   The are async methods to increase performance in IO blocking situations.
"""
from typing import List
from pydantic.error_wrappers import ValidationError

from identity.domain.users import User
from identity.domain.pagination import Page
from identity.services.exceptions import InvalidEmailFormatException, UserAlreadyExistsException, UserDoesNotExistException
from identity.services.security import get_password_hash
from identity.services.uow.users import UsersAbstractUnitOfWork


async def new_user(email: str, plain_password: str, uow: UsersAbstractUnitOfWork) -> User:
    """Creates a new user

    :param email: email of the user. It must be unique.
    :type email: str
    :param plain_password: password of the user in plain text.
    :type plain_password: str
    :param uow: Unit of work for users.
    :type uow: UsersAbstractUnitOfWork
    :raises InvalidEmailFormatException:
    :raises UserAlreadyExistsException:
    :return: a User object.
    :rtype: User
    """
    try:
        hashed_password = get_password_hash(plain_password)
        new_user_param = User(email=email, password=hashed_password)
    except ValidationError as ve:
        raise InvalidEmailFormatException()

    async with uow:
        if await uow.users.get_user(email) is not None:
            raise UserAlreadyExistsException()

        new_user = await uow.users.add_user(new_user_param)
        await uow.commit()
    return new_user


async def get_user(email: str, uow: UsersAbstractUnitOfWork) -> User:
    """Gets a user by email

    :param email: email of the user you want to get
    :type email: str
    :param uow: Unit of work for users.
    :type uow: UsersAbstractUnitOfWork
    :raises UserDoesNotExistException: 
    :return: a User object.
    :rtype: User
    """
    async with uow:
        user = await uow.users.get_user(email)
        if user is None:
            raise UserDoesNotExistException()
        return user


async def list_users(uow: UsersAbstractUnitOfWork) -> List[User]:
    """Returns a list with all users

    :param uow: Unit of work for users.
    :type uow: UsersAbstractUnitOfWork
    :return: returns a list with all users.
    :rtype: List[User]
    """
    async with uow:
        return await uow.users.list_users()


async def list_paginated_users(uow: UsersAbstractUnitOfWork, page:int = 1, page_size:int = 100_000) -> Page[User]:
    """_summary_

    :param uow: Unit of work for users.
    :type uow: UsersAbstractUnitOfWork
    :param page: number of the page starting from 1, defaults to 1
    :type page: int, optional
    :param page_size: number of elements per page, defaults to 100_000
    :type page_size: int, optional
    :return: A Page object with required information
    :rtype: Page[User]
    """
    async with uow:
        return await uow.users.list_paginated_users(page, page_size)
    

async def validate_user(email: str, uow: UsersAbstractUnitOfWork) -> User:
    """Validates the email of a user. It is first step required to allow the user to be active.

    :param email: user's email
    :type email: str
    :param uow: Unit of work for users.
    :type uow: UsersAbstractUnitOfWork
    :raises UserDoesNotExistException:
    :return: The validated user object
    :rtype: User
    """
    async with uow:
        user = await uow.users.get_user(email)
        if user is None:
            raise UserDoesNotExistException()
        user.validate()
        user = await uow.users.update_user(user)
        await uow.commit()
        return user


async def enable_user(email: str, uow: UsersAbstractUnitOfWork) -> User:
    """Activates an user by email.

    :param email: user's email
    :type email: str
    :param uow: Unit of work for users.
    :type uow: UsersAbstractUnitOfWork
    :raises UserDoesNotExistException: 
    :return: The user enabled
    :rtype: User
    """
    async with uow:
        user = await uow.users.get_user(email)
        if user is None:
            raise UserDoesNotExistException()
        user.enable()
        user = await uow.users.update_user(user)
        await uow.commit()
        return user


async def disable_user(email: str, uow: UsersAbstractUnitOfWork) -> User:
    """Disables a user by email so that it cannot be used

    :param email: user's email
    :type email: str
    :param uow: Unit of work for users.
    :type uow: UsersAbstractUnitOfWork
    :raises UserDoesNotExistException: 
    :return: The disabled user
    :rtype: User
    """
    async with uow:
        user = await uow.users.get_user(email)
        if user is None:
            raise UserDoesNotExistException()
        user.disable()
        user = await uow.users.update_user(user)
        await uow.commit()
        return user
