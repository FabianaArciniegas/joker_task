from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str
    DB_CONNECTION: str
    DB_NAME: str
    API_STR: str = "/api"
    SECRET_KEY: str
    SECRET_KEY_REFRESH: str


settings = Settings()
