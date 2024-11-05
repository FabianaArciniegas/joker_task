from pydantic import BaseModel, EmailStr


class UserCreation(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    password: str
