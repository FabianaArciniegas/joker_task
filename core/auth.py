from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from core.errors import UnauthorizedError
from models.responde_model import LocationError
from models.users import TokenData
from utils.tokens_jwt import decode_token, TokenType

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


async def get_current_user(
        access_token: Annotated[str, Depends(oauth2_scheme)]
) -> TokenData:
    payload = await decode_token(access_token, TokenType.access_token)
    if not payload or "id" not in payload:
        raise UnauthorizedError(message="Invalid credentials", location=LocationError.Headers)
    token_data = TokenData(**payload)
    return token_data


async def verify_active_user(user_id: str, token_data: TokenData):
    if token_data.id != user_id:
        raise UnauthorizedError(message="Access denied: You are not allowed to access this resource",
                                location=LocationError.Headers)
