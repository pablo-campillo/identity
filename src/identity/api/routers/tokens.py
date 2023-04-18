from datetime import timedelta
from typing import Annotated
from jose import JWTError, jwt
from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from pydantic import ValidationError

from identity.config import get_jwt_algorithm, get_jwt_secret_key
from identity.api.schemas.tokens import Token, TokenData
from identity.config import get_jwt_access_tocken_expire_minutes
from identity.domain.users import User
from identity.services.security import authenticate_user, create_access_token
from identity.services.uow.users import UsersSqlAlchemyUnitOfWork
from identity.adapters.db.session import async_session
from identity.services import users as user_services

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="v1/token",
    scopes={
    "me": "Read information about the current user.", 
    "users:read": "Read information about all users",
    "admin": "Read items."
    },
)

uow = UsersSqlAlchemyUnitOfWork(async_session)

async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, get_jwt_secret_key(), algorithms=[get_jwt_algorithm()])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = await user_services.get_user(token_data.username, uow)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])]
):
    if not current_user.is_active():
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await authenticate_user(form_data.username, form_data.password, uow)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=get_jwt_access_tocken_expire_minutes())
    access_token = create_access_token(
        data={"sub": user.email, "scopes": form_data.scopes}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
