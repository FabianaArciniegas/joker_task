from pydantic import BaseModel, EmailStr


class UserCreation(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: str | None = None
    full_name: str | None = None
    email: EmailStr | None = None
    profile_picture: str | None = None