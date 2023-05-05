from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from identity.domain.utils import utcnow


class User(BaseModel):
    """Represents a user (identity)

    A user is identified by an email that must be unique.
    First a user email should be validated using :func:`validate`
    and then the user should be activated calling :func:`enable` method.

    :param created_at: utc datetime when the user was created
    :type create_at: datetime
    :param updated_at: utc datetime when the user was last updated
    :type updated_at: datetime
    :param email: email address of the user.
    :type email: EmailStr
    :param password: hashed password of the user
    :type password: str
    :param active: if `True` the user can be used. Default it is `False`.
    :type active: bool
    :param validated: if `True` the email address of the user has been validated.
                      Default it is `False`.
    :type validated: bool
    """
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
        """Marks the email address of the user as valid"""
        self.updated_at = utcnow()
        self.validated = True

    def is_validated(self) -> bool:
        """Returns if the emails address has been validated

        :return: `True` if the emails address has been validated, `False` otherwise.
        :rtype: bool
        """
        return self.validated
    
    def disable(self):
        """Disables the user and cannot be used
        """
        self.updated_at = utcnow()
        self.active = False
    
    def enable(self):
        """Enables the user to be available for being used
        """
        self.updated_at = utcnow()
        self.active = True
    
    def is_active(self) -> bool:
        """Returns if the user is active

        :return: `True` if the user is active, `False` otherwise.
        :rtype: bool
        """
        return self.active
