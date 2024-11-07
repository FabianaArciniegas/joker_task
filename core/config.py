from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str
    DB_CONNECTION: str
    DB_NAME: str
    API_STR: str = "/api"
    SECRET_KEY: str
    SECRET_KEY_REFRESH: str
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: EmailStr
    SMTP_PASSWORD: str


settings = Settings()
