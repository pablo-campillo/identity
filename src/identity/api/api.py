from fastapi import APIRouter

from identity.api.routers import tokens, users

api_router = APIRouter()

api_router.include_router(tokens.router, prefix="/token", tags=["SignIn"])
api_router.include_router(users.router, prefix="/users", tags=["Identities"])