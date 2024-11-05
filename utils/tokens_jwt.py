from datetime import datetime, timedelta
from enum import Enum

from jose import jwt

from core.config import settings

SECRET_KEY = settings.SECRET_KEY
SECRET_KEY_REFRESH = settings.SECRET_KEY_REFRESH
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


class TokenType(str, Enum):
    access_token = "access_token"
    refresh_token = "refresh_token"


async def create_token(data: dict, token_type: TokenType):
    to_encode = data.copy()
    if token_type == TokenType.access_token:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    if token_type == TokenType.refresh_token:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY_REFRESH, algorithm=ALGORITHM)
    return encoded_jwt
