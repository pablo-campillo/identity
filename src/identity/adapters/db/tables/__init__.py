from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

from identity.adapters.db.tables.users import *
