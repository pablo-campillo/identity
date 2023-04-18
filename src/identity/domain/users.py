from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from identity.domain.utils import utcnow


class User(BaseModel):
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    email: EmailStr
    password: str
    active: bool = False
    validated: bool = False

    class Config:
        orm_mode = True

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return other.email == self.email

    def __hash__(self):
        return hash(self.email)

    def validate(self):
        self.updated_at = utcnow()
        self.validated = True

    def is_validated(self):
        return self.validated
    
    def disable(self):
        self.updated_at = utcnow()
        self.active = False
    
    def enable(self):
        self.updated_at = utcnow()
        self.active = True
    
    def is_active(self):
        return self.active
