""" Module containing the AppSettings class that represents
the application's configuration settings."""
import multiprocessing

from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    app_port: int = 8000
    app_host: str = 'localhost'
    reload: bool = True
    cpu_count: int | None = None
    postgres_dsn: PostgresDsn = MultiHostUrl(
        'postgresql+asyncpg://postgres:postgres@localhost:5432/cicd-47-db')
    jwt_secret: str = 'SECRET'
    algorithm: str = 'HS256'

    class Config:
        _env_file = ".env"
        _extra = 'allow'


app_settings = AppSettings()

# набор опций для запуска сервера
uvicorn_options = {
    "host": app_settings.app_host,
    "port": app_settings.app_port,
    "workers": app_settings.cpu_count or multiprocessing.cpu_count(),
    "reload": app_settings.reload
}
