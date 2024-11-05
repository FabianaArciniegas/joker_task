from pydantic import EmailStr

from models.base_model import BaseModelDB


class UsersModel(BaseModelDB):
    _collection_name = 'users'
    username: str
    full_name: str
    email: EmailStr
    password: str
    profile_picture: str = "/static/profile_pictures/default_profile_picture.png"
