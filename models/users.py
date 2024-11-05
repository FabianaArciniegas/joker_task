from pydantic import EmailStr, BaseModel

from models.base_model import BaseModelDB


class UsersModel(BaseModelDB):
    _collection_name = 'users'
    username: str
    full_name: str
    email: EmailStr
    password: str
    profile_picture: str = "/static/profile_pictures/default_profile_picture.png"
    refresh_token: str


class TokenData(BaseModel):
    id: str
    username: str
    full_name: str
    email: str
