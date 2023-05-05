"""Module that contains classes for managing serialization of users"""

import abc
from typing import List, Union
from pydantic import parse_obj_as
from sqlalchemy import select, func

from identity.domain.users import User
from identity.domain.pagination import Page
from identity.adapters.db.tables import users as db_users


class UsersAbstractRepository(abc.ABC):
    """Abstract class that provides methods for managing users"""

    @abc.abstractmethod
    async def add_user(self, user: User) -> User:
        """Adds a new user

        :param user: user entity to be added
        :type user: User
        :return: the user added
        :rtype: User
        """
        pass

    @abc.abstractmethod
    async def update_user(self, user: User) -> User:
        """Updates all attributes of an user

        :param user: User to be updated
        :type user: User
        :return: the updated user
        :rtype: User
        """
        pass

    @abc.abstractmethod
    async def get_user(self, email: str) -> User:
        """Gets a user by email

        :param email: email address of the user
        :type email: str
        :return: user requested
        :rtype: User
        """
        pass

    @abc.abstractmethod
    async def list_users(self) -> List[User]:
        """List all users

        :return: a list with all users stored
        :rtype: List[User]
        """
        pass

    @abc.abstractmethod
    async def list_paginated_users(page: int, page_size: int) -> Page[User]:
        """Gets users by chunks

        :param page: number of page, min valid value is 1.
        :type page: int
        :param page_size: Number of users per page, min valid value is 1.
        :type page_size: int
        :return: a Page object that contains a list of users
        :rtype: Page[User]
        """
        pass


class UsersSqlAlchemyRepository(UsersAbstractRepository):
    """Repository for managing users in a database using sqlalchemy"""
    def __init__(self, session):
        self.session = session

    async def add_user(self, user: User) -> User:
        db_user = db_users.User(**user.dict())
        self.session.add(db_user)
        return User.from_orm(db_user)

    async def update_user(self, user: User) -> User:
        db_user = await self.session.get(db_users.User, user.email)
        for field_name in user.__fields_set__:
            setattr(db_user, field_name, getattr(user, field_name))
        return User.from_orm(db_user)

    async def get_user(self,  email: str) -> Union[User, None]:
        db_user = await self.session.get(db_users.User, email)
        if db_user:
            return User.from_orm(db_user)

    async def list_users(self) -> List[User]:
        stmt = select(db_users.User).order_by(db_users.User.updated_at.desc())
        result = await self.session.execute(stmt)
        return [User.from_orm(db_user[0]) for db_user in result]

    async def list_paginated_users(self, page:int, page_size:int) -> Page[User]:
        stmt = select(db_users.User).order_by(db_users.User.updated_at.desc())
        items = (await self.session.execute(stmt.limit(page_size).offset((page - 1) * page_size))).all()
        total = (await self.session.execute(select(func.count()).select_from(db_users.User))).scalar()
        return Page(items, page, page_size, total)
