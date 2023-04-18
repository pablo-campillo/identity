
from datetime import datetime
from pydantic import BaseModel, EmailStr


class IdentityBase(BaseModel):
    class Config:
        orm_mode = True


class NewUser(IdentityBase):
    username: EmailStr
    password: str


class User(IdentityBase):
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    email: EmailStr
    active: bool
    validated: bool
