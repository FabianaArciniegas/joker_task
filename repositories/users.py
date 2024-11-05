from pydantic import EmailStr

from models.users import UsersModel
from repositories.base_repository import BaseRepository


class UsersRepository(BaseRepository[UsersModel]):
    _entity_model = UsersModel

    async def verify_username(self, username: str, raise_exception: bool = True) -> None:
        user = await self.collection.find_one({'username': username})
        if user and raise_exception:
            raise ValueError(f'The user {username} is not available, it already exists')

    async def verify_email(self, email: EmailStr, raise_exception: bool = True) -> None:
        user = await self.collection.find_one({'email': email})
        if user and raise_exception:
            raise ValueError(f'The email {email} is not available, it already exists')
