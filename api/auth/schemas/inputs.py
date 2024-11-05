from pydantic import BaseModel


class UserLogin(BaseModel):
    username_or_email: str
    password: str