import re

from pydantic import BaseModel, model_validator
from typing_extensions import Self

from core.errors import InvalidCredentialsError, InvalidParameterError
from models.responde_model import LocationError


class UserLogin(BaseModel):
    username_or_email: str
    password: str


class Token(BaseModel):
    token: str


class UserEmail(BaseModel):
    email: str


class UserResetPassword(BaseModel):
    password_reset_token: str
    user_id: str
    new_password: str
    confirm_password: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        new_password = self.new_password
        confirm_password = self.confirm_password
        if new_password is not None and confirm_password is not None and new_password != confirm_password:
            raise InvalidCredentialsError(message="Passwords don't match", location=LocationError.Body)
        return self

    @model_validator(mode="after")
    def validate_password(self) -> Self:
        password = self.new_password
        if len(password) < 8:
            raise InvalidParameterError(message="Password must be at least 8 characters", location=LocationError.Body)
        if not re.search(r"[A-Z]", password):
            raise InvalidParameterError(message="Password must contain at least one uppercase letter",
                                        location=LocationError.Body)
        if not re.search(r"[a-z]", password):
            raise InvalidParameterError(message="Password must contain at least one lowercase letter",
                                        location=LocationError.Body)
        if not re.search(r"[0-9]", password):
            raise InvalidParameterError(message="Password must contain at least one number",
                                        location=LocationError.Body)
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise InvalidParameterError(message="Password must contain at least one special character",
                                        location=LocationError.Body)
        return self
