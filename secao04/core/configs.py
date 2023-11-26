from typing import ClassVar

from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta


class Settings(BaseSettings):
    """
    Configurações gerais usadas na aplicação
    """
    API_VI_STR: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/faculdade"
    DBBaseModel: ClassVar[DeclarativeMeta] = declarative_base()

    class Config:
        case_sensitive = True


settings = Settings()
