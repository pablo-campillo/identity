"""This moldule provides clases following the Unit of Work Pattern.
This units of work are transactions for managing users."""
import abc

from identity.adapters.repositories.users import UsersAbstractRepository, UsersSqlAlchemyRepository


class UsersAbstractUnitOfWork(abc.ABC):
    """Base class to construct Unit of works for managing users
    
    It is an Async Context Manager.

    Client must call manually to the :func:`commit` method before
    exit from the context, otherwise, the :func:`rollback` will take effect.

    :param users: repository for managing serialization of users
    :type users: class:`identity.adapters.repositories.users.UsersAbstractRepository`
    """
    users: UsersAbstractRepository

    async def __aexit__(self, *args):
        await self.rollback()

    @abc.abstractmethod
    async def commit(self):
        """Method for saving the changes"""
        pass

    @abc.abstractmethod
    async def rollback(self):
        """Method for undoing the changes"""
        pass


class UsersSqlAlchemyUnitOfWork(UsersAbstractUnitOfWork):
    """Unit of work for making transaction with users in a database using sqlalchemy"""

    def __init__(self, session_factory):
        self.session = session_factory()

    async def __aenter__(self):
        self.users = UsersSqlAlchemyRepository(self.session)
        # return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
