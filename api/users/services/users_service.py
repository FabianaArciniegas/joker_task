from typing import List

from motor.motor_asyncio import AsyncIOMotorDatabase

from api.users.schemas.inputs import UserCreation, UserUpdate, UserChangePassword
from api.users.schemas.outputs import UserResponse
from core.errors import InvalidTokenError
from models.responde_model import LocationError
from repositories.users import UsersRepository
from schemas.api_response import ApiResponse
from services.email_sending_service import EmailSendingService
from utils.security import hash_password, check_password
from utils.tokens_jwt import create_random_token


class UsersService:
    def __init__(self, db: AsyncIOMotorDatabase, api_response: ApiResponse):
        self.db = db
        self.api_response = api_response
        self.user_repository = UsersRepository(self.db)
        self.send_email = EmailSendingService()

    async def create_user(self, user_data: UserCreation) -> UserResponse:
        self.api_response.logger.info("Check if the user already exists")
        await self.user_repository.username_available(user_data.username)
        self.api_response.logger.info("Received data to create user")
        user_add = user_data.model_dump()
        user_add["password"] = await hash_password(user_data.password)
        token_for_email = create_random_token()
        user_add["user_verify_token"] = token_for_email
        created_user = await self.user_repository.create(user_add)
        self.api_response.logger.info("Sending email to user")
        await self.send_email.send_email_to_verify_user(created_user.id, created_user.email, token_for_email,
                                                        created_user.full_name)
        user = UserResponse(**created_user.model_dump())
        return user

    async def verify_user(self, user_id: str, user_token: str) -> UserResponse:
        self.api_response.logger.info("Get user")
        user_found = await self.user_repository.get_by_id(user_id)
        self.api_response.logger.info("Compare tokens")
        if user_found.user_verify_token != user_token:
            raise InvalidTokenError(message="Invalid token", location=LocationError.Query)
        self.api_response.logger.info("Confirm verification and delete token")
        user_found.user_verify_token = None
        user_found.is_verified = True
        verified_user = await self.user_repository.patch(user_id, user_found)
        user = UserResponse(**verified_user.model_dump())
        return user

    async def get_user_by_id(self, user_id: str) -> UserResponse:
        self.api_response.logger.info("Get user")
        user_found = await self.user_repository.get_by_id(user_id)
        user = UserResponse(**user_found.model_dump())
        return user

    async def get_all_users(self) -> List[UserResponse]:
        self.api_response.logger.info("Get all users")
        users_found = await self.user_repository.get_all()
        users = []
        for user in users_found:
            users.append(UserResponse(**user.model_dump()))
        return users

    async def update_user(self, user_id: str, user_data: UserUpdate) -> UserResponse:
        self.api_response.logger.info("Check if data is available")
        await self.user_repository.username_available(user_data.username)
        await self.user_repository.email_available(user_data.email)
        self.api_response.logger.info("Received data to update user")
        updated_user = await self.user_repository.patch(user_id, user_data)
        user = UserResponse(**updated_user.model_dump())
        return user

    async def delete_user(self, user_id: str) -> None:
        self.api_response.logger.info("Delete user")
        await self.user_repository.delete(user_id)

    async def change_password(self, user_id: str, user_password: UserChangePassword) -> UserResponse:
        self.api_response.logger.info("Get user")
        user_found = await self.user_repository.get_by_id(user_id)
        self.api_response.logger.info("Received data to update user")
        await check_password(user_found.password, user_password.current_password)
        user_found.password = await hash_password(user_password.new_password)
        updated_user = await self.user_repository.patch(user_id, user_found)
        user = UserResponse(**updated_user.model_dump())
        return user
