"""Module with security functionalities."""

from datetime import datetime, timedelta
from typing import Union
from passlib.context import CryptContext
from jose import JWTError, jwt

from identity import config
from identity.domain.users import User
from identity.services.uow.users import UsersAbstractUnitOfWork


JWT_SECRET_KEY = config.get_jwt_secret_key()
JWT_ALGORITHM = config.get_jwt_algorithm()
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = config.get_jwt_access_tocken_expire_minutes()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password) -> str:
    """Hashes a plain text password to protect it"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """Creates an access token for a user using the data provided and valid for a period of time.

    :param data: Data that will be enconded in the token.
    :type data: dict
    :param expires_delta: _description_, defaults to None
    :type expires_delta: Union[timedelta, None], optional
    :return: _description_
    :rtype: _type_
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def _verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, password: str, uow: UsersAbstractUnitOfWork) -> Union[User, None]:
    """Checks if the password is correct for the given email.
    If it ok the User object is return, otherwise None.

    :param email: email address of the user
    :type email: str
    :param password: passwor of the user in plain text
    :type password: str
    :param uow: Unit of work for users.
    :type uow: UsersAbstractUnitOfWork
    :return: Return the authenticated user or None, otherwise.
    :rtype: Union[User, None]
    """
    async with uow:
        user = await uow.users.get_user(email)
        if not user:
            return None
        if not _verify_password(password, user.password):
            return None
        return user
