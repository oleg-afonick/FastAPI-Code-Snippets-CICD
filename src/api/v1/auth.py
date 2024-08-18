from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.exceptions import HTTPException

from src.auth.auth import create_access_token
from src.db.db import db_dependency
from src.models import User
from src.schemas.user import UserRegisterSchema, UserLoginSchema
from src.services.auth import reg_user, authenticate_user

auth_router = APIRouter(prefix="/auth", tags=['auth'])


@auth_router.post("/register")
async def register_user(user_data: UserRegisterSchema, db: db_dependency):
    try:
        return await reg_user(user_data=user_data, db=db)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Аn error has occurred: {ex}")


@auth_router.post("/login")
async def login_for_access_token(db: db_dependency,
                                 login_data: UserLoginSchema):
    user: Optional[User] = await authenticate_user(login_data, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={**user.to_dict()}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/token")
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                db: db_dependency):
    user = await authenticate_user(
        UserLoginSchema(email=form_data.username, password=form_data.password),
        db=db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user.")
    access_token = create_access_token(
        data={**user.to_dict()}
    )
    return {'access_token': access_token, 'token_type': 'bearer'}
