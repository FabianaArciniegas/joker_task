from pydantic import BaseModel


class TokensResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
