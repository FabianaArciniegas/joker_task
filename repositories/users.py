from typing import Union

from pydantic import EmailStr

from core.errors import NotAvailableError, InvalidCredentialsError
from models.responde_model import LocationError
from models.users import UsersModel
from repositories.base_repository import BaseRepository, DBModel


class UsersRepository(BaseRepository[UsersModel]):
    _entity_model = UsersModel

    async def username_available(self, username: str, raise_exception: bool = True) -> None:
        self.api_response.logger.info("Checking availability")
        username = await self.collection.find_one({'username': username})
        if username and raise_exception:
            raise NotAvailableError(message=f"The user {username} is not available, it already exists",
                                    location=LocationError.Body)

    async def email_available(self, email: EmailStr, raise_exception: bool = True) -> None:
        self.api_response.logger.info("Checking availability")
        user = await self.collection.find_one({'email': email})
        if user and raise_exception:
            raise NotAvailableError(message=f'The email {email} is not available, it already exists',
                                    location=LocationError.Body)

    async def confirm_if_username_or_email_exists(self, username_or_email: Union[str, EmailStr],
                                                  raise_exception: bool = True) -> None:
        user = await self.collection.find_one({"$or": [{'username': username_or_email}, {'email': username_or_email}]})
        if not user and raise_exception:
            raise InvalidCredentialsError(message="Invalid credentials", location=LocationError.Body)

    async def get_by_username_or_email(self, username_or_email: Union[str, EmailStr]) -> DBModel:
        user = await self.collection.find_one({"$or": [{'username': username_or_email}, {'email': username_or_email}]})
        return self._entity_model.model_validate(user)
