from typing import List

from motor.motor_asyncio import AsyncIOMotorDatabase

from api.users.schemas.inputs import UserCreation, UserUpdate
from api.users.schemas.outputs import UserResponse
from repositories.users import UsersRepository
from utils.security import hash_password


class UsersService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.user_repository = UsersRepository(self.db)

    async def create_user(self, user_data: UserCreation) -> UserResponse:
        print("Check if the user already exists")
        await self.user_repository.username_available(user_data.username)
        user_data.password = await hash_password(user_data.password)
        print("Received data to create user in service")
        created_user = await self.user_repository.create(user_data.model_dump())
        user = UserResponse(**created_user.model_dump())
        return user

    async def get_user_by_id(self, user_id: str) -> UserResponse:
        print("Get user from database")
        user_found = await self.user_repository.get_by_id(user_id)
        user = UserResponse(**user_found.model_dump())
        return user

    async def get_all_users(self) -> List[UserResponse]:
        print("Get all users from database")
        users_found = await self.user_repository.get_all()
        users = []
        for user in users_found:
            users.append(UserResponse(**user.model_dump()))
        return users

    async def update_user(self, user_id: str, user_data: UserUpdate) -> UserResponse:
        print("Check if data is available")
        await self.user_repository.username_available(user_data.username)
        await self.user_repository.email_available(user_data.email)
        print("Received data to update user in service")
        updated_user = await self.user_repository.patch(user_id, user_data)
        user = UserResponse(**updated_user.model_dump())
        return user

    async def delete_user(self, user_id: str) -> None:
        print("Delete user from database")
        await self.user_repository.delete(user_id)
        return
