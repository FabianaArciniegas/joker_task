import re

from pydantic import BaseModel, EmailStr, model_validator
from typing_extensions import Self

from core.errors import InvalidParameterError, InvalidCredentialsError
from models.responde_model import LocationError


class UserCreation(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    password: str

    @model_validator(mode="after")
    def validate_password(self) -> Self:
        password = self.password
        if len(password) < 8:
            raise InvalidParameterError(message="Password must be at least 8 characters", location=LocationError.Body)
        if not re.search(r'[a-z]', password):
            raise InvalidParameterError(message="Password must contain at least one lowercase letter",
                                        location=LocationError.Body)
        if not re.search(r'[A-Z]', password):
            raise InvalidParameterError(message="Password must contain at least one uppercase letter",
                                        location=LocationError.Body)
        if not re.search(r'[0-9]', password):
            raise InvalidParameterError(message="Password must contain at least one number",
                                        location=LocationError.Body)
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            raise InvalidParameterError(message="Password must contain at least one special character",
                                        location=LocationError.Body)
        return self


class UserUpdate(BaseModel):
    username: str | None = None
    full_name: str | None = None
    email: EmailStr | None = None
    profile_picture: str | None = None


class UserChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        new_password = self.new_password
        confirm_password = self.confirm_password
        if new_password is not None and confirm_password is not None and new_password != confirm_password:
            raise InvalidCredentialsError("Passwords don't match", location=LocationError.Body)
        return self

    @model_validator(mode="after")
    def validate_password(self) -> Self:
        password = self.new_password
        if len(password) < 8:
            raise InvalidParameterError(message="Password must be at least 8 characters", location=LocationError.Body)
        if not re.search(r'[a-z]', password):
            raise InvalidParameterError(message="Password must contain at least one lowercase letter",
                                        location=LocationError.Body)
        if not re.search(r'[A-Z]', password):
            raise InvalidParameterError(message="Password must contain at least one uppercase letter",
                                        location=LocationError.Body)
        if not re.search(r'[0-9]', password):
            raise InvalidParameterError(message="Password must contain at least one number",
                                        location=LocationError.Body)
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            raise InvalidParameterError(message="Password must contain at least one special character",
                                        location=LocationError.Body)
        return self
