from typing import List, Annotated

from fastapi import APIRouter, Request, Response, Depends

from api.users.schemas.inputs import UserCreation, UserUpdate, UserChangePassword
from api.users.schemas.outputs import UserResponse
from api.users.services.users_service import UsersService
from core.auth import get_current_user
from models.responde_model import ResponseModel
from models.users import TokenData
from schemas.api_response import ApiResponse
from utils.reponse_handler import response_handler

users_router: APIRouter = APIRouter(prefix='/users')


@users_router.post(
    path="",
    tags=['users'],
    description='Create a new user',
)
@response_handler()
async def create_user(
        request: Request,
        response: Response,
        user_data: UserCreation,
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[UserResponse]:
    api_response.logger.info("Received data to create user")
    user_service = UsersService(request.app.database, api_response)
    user = await user_service.create_user(user_data)
    api_response.logger.info(f"User created successfully: {user}")
    return user


@users_router.get(
    path="/verify-user",
    tags=['users'],
    description='Verify user',
)
@response_handler()
async def verify_user(
        request: Request,
        response: Response,
        _id: str,
        token: str,
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[UserResponse]:
    api_response.logger.info("Received data to verify user")
    user_service = UsersService(request.app.database, api_response)
    user = await user_service.verify_user(_id, token)
    api_response.logger.info(f"User verified successfully: {user}")
    return user


@users_router.get(
    path="/id={user_id}",
    tags=['users'],
    description='Get user by id',
)
@response_handler()
async def get_user_by_id(
        request: Request,
        response: Response,
        user_id: str,
        token_data: Annotated[TokenData, Depends(get_current_user)],
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[UserResponse]:
    api_response.logger.info("Received data to get user")
    user_service = UsersService(request.app.database, api_response, token_data)
    user = await user_service.get_user_by_id(user_id)
    api_response.logger.info(f"User found successfully: {user}")
    return user


@users_router.get(
    path="",
    tags=['users'],
    description='Get all users',
)
@response_handler()
async def get_all_users(
        request: Request,
        response: Response,
        token_data: Annotated[TokenData, Depends(get_current_user)],
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[List[UserResponse]]:
    api_response.logger.info("Received data to get all users")
    user_service = UsersService(request.app.database, api_response)
    users = await user_service.get_all_users()
    api_response.logger.info(f"All users found successfully: {users}")
    return users


@users_router.patch(
    path="/id={user_id}",
    tags=['users'],
    description='Update user',
)
@response_handler()
async def update_user(
        request: Request,
        response: Response,
        user_id: str,
        user_data: UserUpdate,
        token_data: Annotated[TokenData, Depends(get_current_user)],
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[UserResponse]:
    api_response.logger.info("Received data to update user")
    user_service = UsersService(request.app.database, api_response, token_data)
    user = await user_service.update_user(user_id, user_data)
    api_response.logger.info(f"User updated successfully: {user}")
    return user


@users_router.delete(
    path="/id={user_id}",
    tags=['users'],
    description='Delete user',
)
@response_handler()
async def delete_user(
        request: Request,
        response: Response,
        user_id: str,
        token_data: Annotated[TokenData, Depends(get_current_user)],
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel:
    api_response.logger.info("Received data to delete user")
    user_service = UsersService(request.app.database, api_response, token_data)
    await user_service.delete_user(user_id)
    api_response.logger.info(f"User deleted successfully: {user_id}")
    return


@users_router.patch(
    path="/change-password/id={user_id}",
    tags=['users'],
    description='Change password',
)
@response_handler()
async def change_password(
        request: Request,
        response: Response,
        user_id: str,
        user_password: UserChangePassword,
        token_data: Annotated[TokenData, Depends(get_current_user)],
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[UserResponse]:
    api_response.logger.info("Received data to change the user password")
    user_service = UsersService(request.app.database, api_response, token_data)
    user = await user_service.change_password(user_id, user_password)
    api_response.logger.info(f"Password updated successfully: {user}")
    return user
