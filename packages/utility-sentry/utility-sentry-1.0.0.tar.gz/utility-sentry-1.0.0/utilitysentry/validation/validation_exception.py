"""This module provide functionality to create custom exception.

This module contains following classes:-
    `UtilityError`:- This class is responsible for custom exception.
    `UtilityGenericError`:- This class is responsible for generic exception.
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
    """Custom exception class validation generic exceptions."""

    def __init__(self, base_exception=None):
        """Initialize a UtilityGenericError instance.

        Args:
            base_exception (obj): An exception object.
        """
        caller_frame = inspect.currentframe().f_back
        source = ExceptionSource().get_source(caller_frame)
        super().__init__(
            ("UV-101", "GENERIC_ERROR", HTTPStatus.INTERNAL_SERVER_ERROR),
            "Encounter some internal error. Please contact administrator.",
            source,
            base_exception
        )


class UtilityValidationInitializationError(UtilityError):
    """Utility validation class initialization exceptions."""

    def __init__(self, message):
        """Initialize a UtilityValidationInitializationError instance."""
        caller_frame = inspect.currentframe().f_back
        source = ExceptionSource().get_source(caller_frame)
        super().__init__(
            ("UV-102", "UTILITY_VALIDATION_INITIALIZATION_ERROR",
             HTTPStatus.BAD_REQUEST), message, source=source
        )


class UtilityValidationFailError(UtilityError):
    """Utility validation fail exceptions."""

    def __init__(self, message):
        """Initialize a UtilityValidationFailError instance."""
        caller_frame = inspect.currentframe().f_back
        source = ExceptionSource().get_source(caller_frame)
        super().__init__(
            ("UV-103", "UTILITY_VALIDATION_FAIL_ERROR",
             HTTPStatus.BAD_REQUEST), message, source=source
        )
