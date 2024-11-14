from typing import Annotated

from fastapi import APIRouter, Request, Response, Depends

from api.auth.schemas.inputs import UserLogin, Token, UserEmail, UserResetPassword
from api.auth.schemas.outputs import TokensResponse
from api.auth.services.auth_service import AuthService
from api.users.schemas.outputs import UserResponse
from core.auth import get_current_user
from models.responde_model import ResponseModel
from models.users import TokenData
from schemas.api_response import ApiResponse
from utils.reponse_handler import response_handler

auth_router: APIRouter = APIRouter(prefix="/auth")


@auth_router.post(
    path="/login",
    tags=["auth"],
    description="Login a user",
)
@response_handler()
async def login(
        request: Request,
        response: Response,
        user_login: UserLogin,
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[TokensResponse]:
    api_response.logger.info("Received data to log")
    auth_service = AuthService(request.app.database, api_response)
    user_tokens = await auth_service.login(user_login)
    api_response.logger.info(f"User successfully logged in: {user_login.username_or_email}")
    return user_tokens


@auth_router.post(
    path="/refresh-token",
    tags=["auth"],
    description="Refresh token",
)
@response_handler()
async def refresh_token(
        request: Request,
        response: Response,
        refresh_token: Token,
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[TokensResponse]:
    api_response.logger.info("Received data to refresh token")
    auth_service = AuthService(request.app.database, api_response)
    user_tokens = await auth_service.refresh_token(refresh_token.token)
    api_response.logger.info(f"Refresh token successfully refreshed: {user_tokens.refresh_token}")
    return user_tokens


@auth_router.post(
    path="/logout",
    tags=["auth"],
    description="Logout a user",
)
@response_handler()
async def logout(
        request: Request,
        response: Response,
        token_data: Annotated[TokenData, Depends(get_current_user)],
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel:
    api_response.logger.info("Received data to logout")
    auth_service = AuthService(request.app.database, api_response)
    await auth_service.logout(token_data.id)
    api_response.logger.info(f"User successfully logged out: {token_data.id}")
    return


@auth_router.post(
    path="/forgot-password",
    tags=["auth"],
    description="Forgot password",
)
@response_handler()
async def forgot_password(
        request: Request,
        response: Response,
        user_email: UserEmail,
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel:
    api_response.logger.info("Received data to forgot password")
    auth_service = AuthService(request.app.database, api_response)
    await auth_service.forgot_password(user_email.email)
    api_response.logger.info(f"Message successfully sent to: {user_email.email}")
    return


@auth_router.post(
    path="/reset-password",
    tags=["auth"],
    description="Reset password",
)
@response_handler()
async def reset_password(
        request: Request,
        response: Response,
        user_password: UserResetPassword,
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[UserResponse]:
    api_response.logger.info("Received data to reset password")
    auth_service = AuthService(request.app.database, api_response)
    updated_password = await auth_service.reset_password(user_password)
    api_response.logger.info(f"Password updated successfully")
    return updated_password
