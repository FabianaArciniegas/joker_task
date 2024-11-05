from motor.motor_asyncio import AsyncIOMotorDatabase

from api.auth.schemas.inputs import UserLogin
from api.auth.schemas.outputs import TokensResponse
from models.users import TokenData
from repositories.users import UsersRepository
from utils.security import check_password
from utils.tokens_jwt import create_token, TokenType


class AuthService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.user_repository = UsersRepository(self.db)

    async def login(self, user_login: UserLogin)->TokensResponse:
        print("Check if user or email exists")
        await self.user_repository.confirm_if_username_or_email_exists(user_login.username_or_email)
        print("Receiving data to log in user ")
        user_found = await self.user_repository.get_by_username_or_email(user_login.username_or_email)
        await check_password(user_found.password, user_login.password)
        token_data = TokenData(**user_found.model_dump())
        access_token = await create_token(data=token_data.model_dump(), token_type=TokenType.access_token)
        refresh_token = await create_token(data=token_data.model_dump(), token_type=TokenType.refresh_token)
        user_found.refresh_token = refresh_token
        await self.user_repository.patch(user_found.id, user_found)
        return TokensResponse(access_token=access_token, refresh_token=refresh_token)

