from fastapi import APIRouter, Request, Response

from api.auth.schemas.inputs import UserLogin
from api.auth.schemas.outputs import TokensResponse
from api.auth.services.auth_service import AuthService

auth_router:APIRouter = APIRouter(prefix="/auth")

@auth_router.post(
    path="/login",
    tags=["login"],
    description="Login a user",
)
async def login(
        request: Request,
        response: Response,
        user_login: UserLogin
)->TokensResponse:
    print("Received data to log in controller")
    auth_service = AuthService(request.app.database)
    tokens = await auth_service.login(user_login)
    print(f"User successfully logged in: {user_login.username_or_email}")
    return tokens