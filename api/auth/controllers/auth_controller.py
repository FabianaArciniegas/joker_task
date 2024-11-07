from fastapi import APIRouter, Request, Response

from api.auth.schemas.inputs import UserLogin, Token, UserEmail, UserResetPassword
from api.auth.schemas.outputs import TokensResponse
from api.auth.services.auth_service import AuthService
from api.users.schemas.outputs import UserResponse

auth_router: APIRouter = APIRouter(prefix="/auth")


@auth_router.post(
    path="/login",
    tags=["login"],
    description="Login a user",
)
async def login(
        request: Request,
        response: Response,
        user_login: UserLogin
) -> TokensResponse:
    print("Received data to log")
    auth_service = AuthService(request.app.database)
    user_tokens = await auth_service.login(user_login)
    print(f"User successfully logged in: {user_login.username_or_email}")
    return user_tokens


@auth_router.post(
    path="/refresh-token",
    tags=["refresh_token"],
    description="Refresh token",
)
async def refresh_token(
        request: Request,
        response: Response,
        refresh_token: Token
) -> TokensResponse:
    print("Received data to refresh token")
    auth_service = AuthService(request.app.database)
    user_tokens = await auth_service.refresh_token(refresh_token.token)
    print(f"Refresh token successfully refreshed: {refresh_token.token}")
    return user_tokens


@auth_router.post(
    path="/forgot-password",
    tags=["forgot_password"],
    description="Forgot password",
)
async def forgot_password(
        request: Request,
        response: Response,
        user_email: UserEmail
):
    print("Received data to forgot password")
    auth_service = AuthService(request.app.database)
    await auth_service.forgot_password(user_email.email)
    print(f"Message successfully sent to: {user_email.email}")
    return


@auth_router.post(
    path="/reset-password",
    tags=["reset_password"],
    description="Reset password",
)
async def reset_password(
        request: Request,
        response: Response,
        user_password: UserResetPassword
) -> UserResponse:
    print("Received data to reset password")
    auth_service = AuthService(request.app.database)
    updated_password = await auth_service.reset_password(user_password)
    print(f"Password updated successfully")
    return updated_password
