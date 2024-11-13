from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    profile_picture: str
