from typing import Optional

from asyncpg import UniqueViolationError
from fastapi import HTTPException
from sqlalchemy import select

from sqlalchemy.orm import joinedload
from starlette import status

from src.auth.auth import bcrypt_context, hash_password, generate_salt
from src.db.db import db_dependency
from src.models import User
from src.schemas.user import UserLoginSchema, UserRegisterSchema


# Регистрация пользователя
async def reg_user(user_data: UserRegisterSchema, db: db_dependency):
    user_salt: str = generate_salt()
    try:
        create_user_statement: User = User(
            **user_data.model_dump(exclude={'password'}),  # распаковываем объект пользователя, исключая пароль
            salt=user_salt,
            hashed_password=hash_password(user_data.password, user_salt)
        )
        # создаем пользователя в базе данных
        db.add(create_user_statement)
        await db.commit()

        return {"response": "User created successfully"}
    except UniqueViolationError:
        # если возникает ошибка UniqueViolationError - считаем, что пользователь с такими данными уже есть
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User with such credentials already exist')
    except Exception as ex:
        raise ex


# Аутентификация пользователя
async def authenticate_user(login_data: UserLoginSchema, db: db_dependency):
    # делаем SELECT запрос в базу данных, для нахождения пользователя по email
    result = await db.execute(select(User)
                              .options(joinedload(User.role))
                              .where(User.email == login_data.email))
    user: Optional[User] = result.scalars().first()

    # пользователь будет авторизован, если он зарегистрирован и ввел корректный пароль
    if not user:
        return False
    if not bcrypt_context.verify(login_data.password + user.salt, user.hashed_password):
        return False
    return user
