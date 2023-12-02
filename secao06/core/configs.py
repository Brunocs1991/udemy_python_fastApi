from typing import ClassVar

from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/faculdade"
    DBBaseModel: ClassVar[DeclarativeMeta] = declarative_base()
    """
    import secrets
    token: str = secrets.token_urlsafe(32)
    """
    JWT_SECRET: str = 'xINw_ZmV60WRbOgviR0lswNEk1qQGmbgLVqpnF2r4GU'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings: Settings = Settings()
