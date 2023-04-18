from typing import Annotated, List

from fastapi import APIRouter, Security, status
from pydantic import EmailStr
from identity.api.routers.tokens import get_current_active_user
from identity.api.schemas.users import NewUser, User
from identity.services.uow.users import UsersSqlAlchemyUnitOfWork
from identity.services import users as user_services
from identity.adapters.db.session import async_session


router = APIRouter()

uow = UsersSqlAlchemyUnitOfWork(async_session)


@router.get("", response_model=List[User])
async def list_all_users(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["users:read"])], 
    status_code=status.HTTP_200_OK
    ) -> List[User]:
    return await user_services.list_users(uow)


@router.post("", response_model=User)
async def register_new_user(
    new_user_data: NewUser, 
    status_code=status.HTTP_201_CREATED
    ) -> User:
    return await user_services.new_user(new_user_data.username, new_user_data.password, uow)


@router.get("/{email}", response_model=User)
async def get_a_user(email: EmailStr, 
                     current_user: Annotated[User, Security(get_current_active_user, scopes=["me"])], 
                     status_code=status.HTTP_200_OK
                     ) -> User:
    return await user_services.get_user(email, uow)


@router.post("/{email}/validate", response_model=User)
async def validate_user_email(email: EmailStr, 
                        current_user: Annotated[User, Security(get_current_active_user, scopes=["admin"])], 
                        status_code=status.HTTP_200_OK
                        ) -> User:
    return await user_services.validate_user(email, uow)


@router.post("/{email}/disable", response_model=User)
async def disable_user(email: EmailStr, 
                       current_user: Annotated[User, Security(get_current_active_user, scopes=["admin"])], 
                       status_code=status.HTTP_200_OK
                       ) -> User:
    return await user_services.disable_user(email, uow)


@router.post("{email}/enable", response_model=User)
async def enable_user(email: EmailStr, 
                      current_user: Annotated[User, Security(get_current_active_user, scopes=["admin"])], 
                      status_code=status.HTTP_200_OK
                      ) -> User:
    return await user_services.enable_user(email, uow)
