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


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
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
    async with uow:
        user = await uow.users.get_user(email)
        if not user:
            return None
        if not _verify_password(password, user.password):
            return None
        return user
