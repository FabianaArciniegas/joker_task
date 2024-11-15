from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import EmailStr

from api.auth.schemas.inputs import UserLogin, UserResetPassword
from api.auth.schemas.outputs import TokensResponse
from api.users.schemas.outputs import UserResponse
from core.errors import InvalidTokenError
from models.responde_model import LocationError
from models.users import TokenData
from repositories.users import UsersRepository
from schemas.api_response import ApiResponse
from services.email_sending_service import EmailSendingService
from utils.security import compare_password, hash_password, verified_user_confirmation
from utils.tokens_jwt import create_token, TokenType, decode_token, create_random_token


class AuthService:
    def __init__(self, db: AsyncIOMotorDatabase, api_response: ApiResponse):
        self.db = db
        self.api_response = api_response
        self.user_repository = UsersRepository(self.db, self.api_response)
        self.send_email = EmailSendingService()

    async def login(self, user_login: UserLogin) -> TokensResponse:
        self.api_response.logger.info("Check if user or email exists")
        await self.user_repository.confirm_if_username_or_email_exists(user_login.username_or_email)
        self.api_response.logger.info("Get user")
        user_found = await self.user_repository.get_by_username_or_email(user_login.username_or_email)
        self.api_response.logger.info("Compare passwords and user confirmation")
        await compare_password(user_found.password, user_login.password)
        await verified_user_confirmation(user_found.is_verified)
        self.api_response.logger.info("Create tokens")
        token_data = TokenData(**user_found.model_dump())
        access_token = await create_token(data=token_data.model_dump(), token_type=TokenType.access_token)
        refresh_token = await create_token(data=token_data.model_dump(), token_type=TokenType.refresh_token)
        self.api_response.logger.info("Save refresh token")
        user_found.refresh_token = refresh_token
        await self.user_repository.patch(user_found.id, user_found)
        return TokensResponse(access_token=access_token, refresh_token=refresh_token)

    async def refresh_token(self, refresh_token: str) -> TokensResponse:
        self.api_response.logger.info("Verify token")
        payload = await decode_token(token=refresh_token, token_type=TokenType.refresh_token)
        self.api_response.logger.info("Get user with token information")
        user_id = payload.get("id")
        user_found = await self.user_repository.get_by_id(user_id)
        self.api_response.logger.info("Compare tokens")
        if user_found.refresh_token != refresh_token:
            raise InvalidTokenError(message="Invalid refresh token", location=LocationError.Body)
        self.api_response.logger.info("Create tokens")
        token_data = TokenData(**user_found.model_dump())
        access_token = await create_token(data=token_data.model_dump(), token_type=TokenType.access_token)
        refresh_token = await create_token(data=token_data.model_dump(), token_type=TokenType.refresh_token)
        self.api_response.logger.info("Save refresh token")
        user_found.refresh_token = refresh_token
        await self.user_repository.patch(user_found.id, user_found)
        return TokensResponse(access_token=access_token, refresh_token=refresh_token)

    async def logout(self, user_id: str) -> None:
        self.api_response.logger.info("Get user")
        user_found = await self.user_repository.get_by_id(user_id)
        self.api_response.logger.info("Delete or disable tokens")
        user_found.refresh_token = None
        await self.user_repository.patch(user_id, user_found)

    async def forgot_password(self, email: EmailStr) -> None:
        self.api_response.logger.info("Check if email exists")
        await self.user_repository.confirm_if_username_or_email_exists(email)
        self.api_response.logger.info("Get user")
        user_found = await self.user_repository.get_by_username_or_email(email)
        self.api_response.logger.info("Save email token")
        token_for_email = create_random_token()
        user_found.password_reset_token = token_for_email
        await self.user_repository.patch(user_found.id, user_found)
        self.api_response.logger.info("Sending email to user")
        await self.send_email.send_email_to_reset_password(user_found.id, email, token_for_email, user_found.full_name)

    async def reset_password(self, user_password: UserResetPassword) -> UserResponse:
        self.api_response.logger.info("Get user")
        user_found = await self.user_repository.get_by_id(user_password.user_id)
        self.api_response.logger.info("Compare tokens")
        if user_found.password_reset_token != user_password.password_reset_token:
            raise InvalidTokenError(message="Invalid password reset token", location=LocationError.Body)
        self.api_response.logger.info("Save new password and delete token")
        user_found.password = await hash_password(user_password.new_password)
        user_found.password_reset_token = None
        updated_user = await self.user_repository.patch(user_found.id, user_found)
        user = UserResponse(**updated_user.model_dump())
        return user

    async def authenticate_user_token(self, form_data) -> TokensResponse:
        self.api_response.logger.info("Get user")
        user_found = await self.user_repository.get_by_username_or_email(form_data.username)
        self.api_response.logger.info("Compare passwords and user confirmation")
        await compare_password(user_found.password, form_data.password)
        await verified_user_confirmation(user_found.is_verified)
        self.api_response.logger.info("Create tokens")
        token_data = TokenData(**user_found.model_dump())
        access_token = await create_token(data=token_data.model_dump(), token_type=TokenType.access_token)
        refresh_token = await create_token(data=token_data.model_dump(), token_type=TokenType.refresh_token)
        return TokensResponse(access_token=access_token, refresh_token=refresh_token)
