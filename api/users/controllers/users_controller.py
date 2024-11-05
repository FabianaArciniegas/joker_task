from typing import List

from fastapi import APIRouter, Request, Response

from api.users.schemas.inputs import UserCreation
from api.users.schemas.outputs import UserBasic
from api.users.services.users_service import UsersService

users_router: APIRouter = APIRouter(prefix='/users')


@users_router.post(
    path="",
    tags=['users'],
    description='Create a new user',
)
async def create_user(
        request: Request,
        response: Response,
        user_data: UserCreation
) -> UserBasic:
    print("Received data to create user in controller")
    user_service = UsersService(request.app.database)
    user = await user_service.create_user(user_data)
    print(f"User created successfully: {user}")
    return user

@users_router.get(
    path="/{user_id}",
    tags=['users'],
    description='Get user by id',
)
async def get_user_by_id(
        request: Request,
        response: Response,
        user_id: str
)-> UserBasic:
    print("Received data to get user in controller")
    user_service = UsersService(request.app.database)
    user = await user_service.get_user_by_id(user_id)
    print(f"User found successfully: {user}")
    return user

@users_router.get(
    path="",
    tags=['users'],
    description='Get all users',
)
async def get_all_users(
        request: Request,
        response: Response
)-> List[UserBasic]:
    print("Get users in controller")
    user_service = UsersService(request.app.database)
    users = await user_service.get_all_users()
    print(f"All users found successfully: {users}")
    return users
