import secrets
from datetime import datetime, timedelta
from enum import Enum

from jose import jwt, ExpiredSignatureError, JWTError

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


async def decode_token(token: str, token_type: TokenType):
    try:
        if token_type == TokenType.access_token:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if token_type == TokenType.refresh_token:
            payload = jwt.decode(token, SECRET_KEY_REFRESH, algorithms=[ALGORITHM])
        if not payload.get("id"):
            raise ValueError("Invalid token")
        return payload
    except ExpiredSignatureError:
        raise ValueError("Token has expired")
    except JWTError:
        raise ValueError("Invalid token or signature verification failed")


def create_random_token():
    return secrets.token_urlsafe()
