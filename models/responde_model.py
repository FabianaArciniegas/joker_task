from enum import Enum
from typing import List, TypeVar, Generic, Optional, Union

from pydantic import BaseModel

DataType = TypeVar('DataType', bound=BaseModel)


class StatusRequest(Enum):
    OK = "OK", 200
    CREATED = "CREATED", 201
    BAD_REQUEST = "BAD_REQUEST", 400
    UNAUTHORIZED = "UNAUTHORIZED", 401
    FORBIDDEN = "FORBIDDEN", 403
    NOT_FOUND = "NOT_FOUND", 404
    METHOD_NOT_ALLOWED = "METHOD_NOT_ALLOWED", 405
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR", 500
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE", 503

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _: str, code: int):
        self._code = code

    def __str__(self):
        return self.value

    @property
    def code(self):
        return self._code


class LocationError(str, Enum):
    Path = "request.path_params"
    Query = "request.query_params"
    Body = "request.body"
    Headers = "request.headers"
    Cookies = "request.cookies"
    Server = "request.server"

    def __str__(self):
        return self.value


class ResponseErrors(BaseModel):
    description: str
    message: str
    location: LocationError


class ResponseModel(BaseModel, Generic[DataType]):
    status: str
    data: Optional[Union[DataType, List[DataType]]] = None
    errors: Optional[List[ResponseErrors]] = None
    process_id: str
