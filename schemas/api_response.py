import uuid
from typing import Any

from core.errors import BaseErrors
from core.logger import logger_api
from models.responde_model import StatusRequest, ResponseErrors, ResponseModel


class ApiResponse:
    def __init__(self):
        self._status = StatusRequest.OK
        self._data = None
        self._errors = []
        self._process_id = str(uuid.uuid4())
        self._logger = logger_api(self._process_id)

    def add_error(self, error: BaseErrors):
        self._errors.append(ResponseErrors(
            description=error.description,
            message=error.message,
            location=error.location,
        ))

    @property
    def status(self):
        return self._status

    @property
    def data(self):
        return self._data

    @property
    def errors(self):
        return self._errors

    @property
    def process_id(self):
        return self._process_id

    @property
    def logger(self):
        return self._logger

    @status.setter
    def status(self, status: StatusRequest):
        self._status = status

    @data.setter
    def data(self, data: Any):
        self._data = data

    @property
    def set_result(self):
        response = ResponseModel(
            status=self._status.value,
            data=self._data,
            errors=self._errors,
            process_id=self._process_id
        ).model_dump()
        return response
