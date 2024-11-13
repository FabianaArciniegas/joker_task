import functools

from fastapi import Request, Response

from core.errors import InvalidParameterError, UnauthorizedError, ForbiddenError, NotFoundError, \
    InvalidCredentialsError, UnExpectedError, InvalidTokenError, NotAvailableError
from models.responde_model import LocationError


def response_handler():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(request: Request, response: Response, *args, **kwargs):
            api_response = kwargs.get("api_response")
            try:
                result = await func(request, response, *args, **kwargs)
                if result:
                    api_response.data = result

            except InvalidParameterError as error:
                api_response.status = error.status
                api_response.add_error(error)
                api_response.logger.error(error)
            except UnauthorizedError as error:
                api_response.status = error.status
                api_response.add_error(error)
                api_response.logger.error(error)
            except ForbiddenError as error:
                api_response.status = error.status
                api_response.add_error(error)
                api_response.logger.error(error)
            except NotFoundError as error:
                api_response.status = error.status
                api_response.add_error(error)
                api_response.logger.error(error)
            except InvalidCredentialsError as error:
                api_response.status = error.status
                api_response.add_error(error)
                api_response.logger.error(error)
            except InvalidTokenError as error:
                api_response.status = error.status
                api_response.add_error(error)
                api_response.logger.error(error)
            except NotAvailableError as error:
                api_response.status = error.status
                api_response.add_error(error)
                api_response.logger.error(error)
            except Exception as error:
                unexpected_error = UnExpectedError(message=error.__str__(), location=LocationError.Server)
                api_response.status = unexpected_error.status
                api_response.add_error(unexpected_error)
                api_response.logger.error(error)

            response.status_code = api_response.status.code
            return api_response.set_result

        return wrapper

    return decorator
