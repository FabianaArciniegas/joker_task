from fastapi import Request
from starlette.responses import JSONResponse

from core.errors import UnauthorizedError, InvalidTokenError, InvalidCredentialsError, InvalidParameterError
from schemas.api_response import ApiResponse


async def auth_validation_error_handler(request: Request, exception: UnauthorizedError):
    api_response = ApiResponse()
    api_response.status = exception.status
    api_response.add_error(exception)
    api_response.logger.error(exception)
    return JSONResponse(content=api_response.set_result, status_code=exception.status.code)


async def invalid_token_error_handler(request: Request, exception: InvalidTokenError):
    api_response = ApiResponse()
    api_response.status = exception.status
    api_response.add_error(exception)
    api_response.logger.error(exception)
    return JSONResponse(content=api_response.set_result, status_code=exception.status.code)


async def invalid_credentials_error_handler(request: Request, exception: InvalidCredentialsError):
    api_response = ApiResponse()
    api_response.status = exception.status
    api_response.add_error(exception)
    api_response.logger.error(exception)
    return JSONResponse(content=api_response.set_result, status_code=exception.status.code)


async def invalid_password_error_handler(request: Request, exception: InvalidParameterError):
    api_response = ApiResponse()
    api_response.status = exception.status
    api_response.add_error(exception)
    api_response.logger.error(exception)
    return JSONResponse(content=api_response.set_result, status_code=exception.status.code)


app_exception_handler = {
    UnauthorizedError: auth_validation_error_handler,
    InvalidTokenError: invalid_token_error_handler,
    InvalidCredentialsError: invalid_credentials_error_handler,
    InvalidParameterError: invalid_password_error_handler,
}
