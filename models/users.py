from typing import List

from pydantic import EmailStr, BaseModel

from models.base_model import BaseModelDB


class UsersModel(BaseModelDB):
    _collection_name = 'users'
    is_verified: bool = False
    username: str
    full_name: str
    email: EmailStr
    password: str
    profile_picture: str = "/static/profile_pictures/default_profile_picture.png"
    workspaces: List[object] = None
    user_verify_token: str | None = None
    refresh_token: str | None = None
    password_reset_token: str | None = None


class TokenData(BaseModel):
    id: str
    username: str
    full_name: str
    email: str
