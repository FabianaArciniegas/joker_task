from models.responde_model import StatusRequest, LocationError


class BaseErrors(Exception):
    def __init__(self, status: str, description: str, message: str, location: LocationError):
        self.status = status
        self.description = description
        self.message = message
        self.location = location

    def __str__(self):
        return f"Error: {self.__class__.__name__} : {self.description} - {self.message}, {self.location}"


class _BaseErrors(BaseErrors):
    status = None
    description = None

    def __init__(self, message: str, location: LocationError):
        self.message = message
        self.location = location
        super().__init__(
            status=self.status,
            description=self.description,
            message=self.message,
            location=self.location
        )


class InvalidParameterError(_BaseErrors):
    status = StatusRequest.BAD_REQUEST
    description = "Parameter error"


class UnauthorizedError(_BaseErrors):
    status = StatusRequest.UNAUTHORIZED
    description = "Unauthorized error"


class ForbiddenError(_BaseErrors):
    status = StatusRequest.FORBIDDEN
    description = "Access is prohibited"


class NotFoundError(_BaseErrors):
    status = StatusRequest.NOT_FOUND
    description = "Not Found"


class InvalidCredentialsError(_BaseErrors):
    status = StatusRequest.UNAUTHORIZED
    description = "Invalid credentials"


class UnExpectedError(_BaseErrors):
    status = StatusRequest.INTERNAL_SERVER_ERROR
    description = "Internal server error"


class InvalidTokenError(_BaseErrors):
    status = StatusRequest.BAD_REQUEST
    description = "Invalid token"


class NotAvailableError(_BaseErrors):
    status = StatusRequest.BAD_REQUEST
    description = "Not available"
