"""This module provide functionality to create custom exception.

This module contains following classes:-
    `UtilityError`:- This class is responsible for custom exception.
    `UtilityGenericError`:- This class is responsible for generic exception.
    `LoggerConfigFileNotFoundError`:- This class is responsible for logger
        config file not found exception.
"""
import inspect
from http import HTTPStatus
from utilitysentry.exception.utility_exception import UtilityException, \
    ExceptionSource


class UtilityError(UtilityException):
    """This class provide functionality to create custom UtilityError."""

    SEPARATOR = "-"

    def __init__(self, error, message, source=None, base_exception=None):
        """Logger Custom Exception constructor.

        This Method is used for initalzing instance variable.

        Args:
            error (object): An object that contains error object information.
            message (string): A string that represents error message.
            source (str): A string that represents exception source location.
            base_exception (obj): An exception object that represents original
                exception.
        """
        UtilityException.__init__(
            self=self,
            error=error,
            message=message,
            source=source,
            base_exception=base_exception
        )


class UtilityGenericError(UtilityError):
    """Custom exception class logger generic exceptions."""

    def __init__(self, base_exception=None):
        """Initialize a UtilityGenericError instance.

        Args:
            base_exception (obj): An exception object.
        """
        caller_frame = inspect.currentframe().f_back
        source = ExceptionSource().get_source(caller_frame)
        super().__init__(
            ("UL-101", "GENERIC_ERROR", HTTPStatus.INTERNAL_SERVER_ERROR),
            "Encounter some internal error. Please contact administrator.",
            source,
            base_exception
        )


class LoggerConfigFileNotFoundError(UtilityError):
    """Custom exception class logger config file not found exceptions."""

    def __init__(self):
        """Initialize a LoggerConfigFileNotFoundError instance."""
        caller_frame = inspect.currentframe().f_back
        source = ExceptionSource().get_source(caller_frame)
        super().__init__(
            ("UL-102", "LOGGER_CONFIGE_FILE_NOT_FOUND",
             HTTPStatus.BAD_REQUEST),
            "Please ensure that the logger config file exists and the path"
            " is correct.",
            source=source
        )
