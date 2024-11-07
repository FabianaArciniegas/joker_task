from typing import List

from fastapi import APIRouter, Request, Response

from api.users.schemas.inputs import UserCreation, UserUpdate, UserChangePassword
from api.users.schemas.outputs import UserResponse
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
) -> UserResponse:
    print("Received data to create user in controller")
    user_service = UsersService(request.app.database)
    user = await user_service.create_user(user_data)
    print(f"User created successfully: {user}")
    return user


@users_router.get(
    path="/verify-user",
    tags=['users'],
    description='Verify user',
)
async def verify_user(
        request: Request,
        response: Response,
        _id: str,
        token: str
) -> UserResponse:
    print("Received data to verify user in controller")
    user_service = UsersService(request.app.database)
    user = await user_service.verify_user(_id, token)
    print(f"User verified successfully: {user}")
    return user


@users_router.get(
    path="/id={user_id}",
    tags=['users'],
    description='Get user by id',
)
async def get_user_by_id(
        request: Request,
        response: Response,
        user_id: str
) -> UserResponse:
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
) -> List[UserResponse]:
    print("Get users in controller")
    user_service = UsersService(request.app.database)
    users = await user_service.get_all_users()
    print(f"All users found successfully: {users}")
    return users


@users_router.patch(
    path="/id={user_id}",
    tags=['users'],
    description='Update user',
)
async def update_user(
        request: Request,
        response: Response,
        user_id: str,
        user_data: UserUpdate
) -> UserResponse:
    print("Received data to update user in controller")
    user_service = UsersService(request.app.database)
    user = await user_service.update_user(user_id, user_data)
    print(f"User updated successfully: {user}")
    return user


@users_router.delete(
    path="/id={user_id}",
    tags=['users'],
    description='Delete user',
)
async def delete_user(
        request: Request,
        response: Response,
        user_id: str
):
    print("Received data to delete user in controller")
    user_service = UsersService(request.app.database)
    await user_service.delete_user(user_id)
    print(f"User deleted successfully: {user_id}")
    return


@users_router.patch(
    path="/change-password/id={user_id}",
    tags=['users'],
    description='Change password',
)
async def change_password(
        request: Request,
        response: Response,
        user_id: str,
        user_password: UserChangePassword,
) -> UserResponse:
    print("Received data to change the user password in controller")
    user_service = UsersService(request.app.database)
    user = await user_service.change_password(user_id, user_password)
    print(f"Password updated successfully: {user}")
    return user
