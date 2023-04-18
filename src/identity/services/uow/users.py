
import abc

from identity.adapters.repositories.users import UsersAbstractRepository, UsersSqlAlchemyRepository


class UsersAbstractUnitOfWork(abc.ABC):
    users: UsersAbstractRepository

    async def __aexit__(self, *args):
        await self.rollback()

    @abc.abstractmethod
    async def commit(self):
        pass

    @abc.abstractmethod
    async def rollback(self):
        pass


class UsersSqlAlchemyUnitOfWork(UsersAbstractUnitOfWork):

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
