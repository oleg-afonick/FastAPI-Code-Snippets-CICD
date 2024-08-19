from fastapi import HTTPException
from sqlalchemy import select
from starlette import status

from auth.auth import bcrypt_context
from db.db import db_dependency
from models import User
from schemas.user import UserCreate, UserRead


async def create_new_user(db: db_dependency, user_data: UserCreate) -> UserRead:
    create_user_request: User = User(
        login=user_data.login,
        email=user_data.email,
        hashed_password=bcrypt_context.hash(user_data.password)
    )

    db.add(create_user_request)
    await db.commit()

    created_user_data: UserRead = await get_user_by_login(db, user_data.login)

    return created_user_data


async def get_user_by_login(db: db_dependency, login: str) -> UserRead:
    statement = select(User).where(User.login == login)
    result = await db.execute(statement)
    user: User = result.scalar()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user with login:{login}")
    return user.to_user_read()
