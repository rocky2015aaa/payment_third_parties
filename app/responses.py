from fastapi import HTTPException
from .constants import RESP_DATA, RESP_STATUS, \
                      RESP_MESSAGE, RESP_ERROR, RESP_METADATA, RESP_RESPONSE


def InternalResponseModel(status: bool, response: str, metadata: object) -> object:  # noqa
    return {
        RESP_STATUS: status,
        RESP_RESPONSE: response,
        RESP_METADATA: metadata
    }


def ResponseModel(data: object, message: str) -> object:
    return {
        RESP_DATA: [data],
        RESP_STATUS: True,
        RESP_MESSAGE: message,
    }


def ResponseModelV2(data: object, message: str) -> object:
    return {
        RESP_DATA: data,
        RESP_STATUS: True,
        RESP_MESSAGE: message,
    }


def ErrorResponseModel(error: str, status: bool, message: str) -> object:
    return {RESP_ERROR: error, RESP_STATUS: status, RESP_MESSAGE: message}


def HTTPExceptionResponse(status_code: int, message: str) -> object:
    return HTTPException(status_code=status_code, detail=message)
