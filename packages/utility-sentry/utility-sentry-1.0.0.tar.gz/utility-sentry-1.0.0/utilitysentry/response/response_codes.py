"""This module will help us to define error codes for custom exception.

This have the following classes:
    - `ResponseCodes` : This class is responsible for custom error codes.
"""
from http import HTTPStatus


class ResponseCodes:
    """Error class to customize error codes and messages.

    This class defines custom error codes, associated error message keys,
    and HTTP status codes.

    A tuple will contain error code, error message key, and HTTP status code
    for custom exception.
    """

    GENERIC_ERROR = (1001, "GENERIC_ERROR", HTTPStatus.INTERNAL_SERVER_ERROR)
