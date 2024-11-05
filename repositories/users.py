from models.users import UsersModel
from repositories.base_repository import BaseRepository


class UsersRepository(BaseRepository[UsersModel]):
    _entity_model = UsersModel

    async def verify_user(self, username: str, raise_exception: bool = True) -> None:
        user = await self.collection.find_one({'username': username})
        if user and raise_exception:
            raise ValueError(f'The user {username} is not available, it already exists')
