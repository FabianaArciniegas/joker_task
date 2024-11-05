from pydantic import BaseModel, EmailStr


class UserBasic(BaseModel):
    username: str
    full_name: str
    email: EmailStr
