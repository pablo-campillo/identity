from datetime import datetime
from sqlalchemy import Boolean, DateTime, Table, Column, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from identity.adapters.db.tables import Base
from identity.domain.users import User


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(primary_key=True)
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    password: Mapped[str] = mapped_column(String(255))
    active: Mapped[bool]
    validated: Mapped[bool]

    def __repr__(self) -> str:
        return f"User(email={self.email!r}, created_at={self.created_at.isoformat()!r}, updated_at={self.updated_at.isoformat()!r}, " \
                f"active={self.active!r}, validated={self.validated!r}, password={self.password!r})"
