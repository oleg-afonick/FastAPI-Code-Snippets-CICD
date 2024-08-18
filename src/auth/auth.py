from calendar import timegm
from datetime import timedelta, datetime
from typing import Annotated, Dict, List

import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status

from src.core.config import app_settings
from src.core.types import RoleEnum

# Секретная фраза для генерации и валидации токенов
JWT_SECRET = app_settings.jwt_secret  # your_super_secret

# Алгоритм хеширования
ALGORITHM = app_settings.algorithm  # 'HS256'

# контекст для валидации и хеширования
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# специальный класс для настройки авторизации в Swagger
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')


# Генерация соли
def generate_salt():
    return bcrypt.gensalt().decode("utf-8")


# Хэширование пароля с использованием соли
def hash_password(password: str, salt: str):
    return bcrypt_context.hash(password + salt)


# создание нового токена
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=60)) -> str:
    # копируем исходные данные, чтобы случайно их не испортить
    to_encode = data.copy()

    # устанавливаем временной промежуток жизни токена
    expire = timegm((datetime.utcnow() + expires_delta).utctimetuple())

    # добавляем время смерти токена
    to_encode.update({"exp": expire})

    # генерируем токен из данных, секрета и алгоритма
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)


# ошибка авторизации пользователя
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


# Получение текущего пользователя из токена доступа
async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        # декод токена доступа
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        # получение необходимых данных о пользователе
        user_data = {"name": payload.get("name"),
                     "email": payload.get("email"),
                     "role": payload.get("role").get("name")}
        if user_data is None:
            raise credentials_exception
    except JWTError:
        # если время жизни токена истекло
        raise credentials_exception
    return user_data

user_dependency = Annotated[dict, Depends(get_current_user)]


def has_role(required_roles: List[RoleEnum]):
    required_roles = [required_role.name for required_role in required_roles]

    def role_checker(current_user: user_dependency) -> Dict:
        if current_user["role"] not in required_roles or current_user["role"] == RoleEnum.ADMIN.name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker
