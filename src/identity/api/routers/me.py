from identity.api.main import app
from identity.api.schemas.users import User


@app.post("me/change_password", response_model=User)
async def change_password() -> User:
    pass


@app.get("me", response_model=User)
async def get_current_user(
    # current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    # return current_user
    pass