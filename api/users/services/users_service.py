from typing import List

from motor.motor_asyncio import AsyncIOMotorDatabase

from api.users.schemas.inputs import UserCreation, UserUpdate, UserChangePassword
from api.users.schemas.outputs import UserResponse
from repositories.users import UsersRepository
from services.email_sending_service import EmailSendingService
from utils.security import hash_password, check_password, verified_user_confirmation
from utils.tokens_jwt import decode_token, create_random_token


class UsersService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.user_repository = UsersRepository(self.db)
        self.send_email = EmailSendingService()

    async def create_user(self, user_data: UserCreation) -> UserResponse:
        print("Check if the user already exists")
        await self.user_repository.username_available(user_data.username)
        print("Received data to create user in service")
        user_add = user_data.model_dump()
        user_add["password"] = await hash_password(user_data.password)
        token_for_email = create_random_token()
        user_add["user_verify_token"] = token_for_email
        created_user = await self.user_repository.create(user_add)
        print("Sending email to user")
        await self.send_email.send_email_to_verify_user(created_user.id, created_user.email, token_for_email)
        user = UserResponse(**created_user.model_dump())
        return user

    async def verify_user(self, user_id: str, user_token: str) -> UserResponse:
        print("Get user from database")
        user_found = await self.user_repository.get_by_id(user_id)
        print("Received data to verify user")
        if user_found.user_verify_token != user_token:
            raise ValueError("Invalid token")
        user_found.user_verify_token = None
        user_found.is_verified = True
        verified_user = await self.user_repository.patch(user_id, user_found)
        user = UserResponse(**verified_user.model_dump())
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

    async def change_password(self, user_id: str, user_password: UserChangePassword) -> UserResponse:
        print("Get user from database")
        user_found = await self.user_repository.get_by_id(user_id)
        print("Received data to update user in service")
        await check_password(user_found.password, user_password.current_password)
        user_found.password = await hash_password(user_password.new_password)
        updated_user = await self.user_repository.patch(user_id, user_found)
        user = UserResponse(**updated_user.model_dump())
        return user
