"""This module provide functionality to create custom exception.

This module contains following classes:-
    `UtilityError`:- This class is responsible for custom exception.
    `UtilityGenericError`:- This class is responsible for generic exception.
    `UtilityConfgiRequiredKeyError`:- This class is responsible for
        GET method required KEY missing exception.
    `UtilityConfgiTooArgumentsError`:- This class is responsible for too many
        arguments exception.
    `UtilityConfigFileNotFoundError`:- This class is responsible for utility
        config file not found exception.
    `UtilityConfigFileENVError`:- This class is responsible for utility
        config file environment variable not exported exception.
    `UtilityConfigKeyNotExistsError`:- This class is responsible for utility
        config KEY doesn't exists error.
"""
import inspect
from http import HTTPStatus
from utilitysentry.exception.utility_exception import UtilityException, \
    ExceptionSource


class UtilityError(UtilityException):
    """This class provide functionality to create custom UtilityError."""

    SEPARATOR = "-"

    def __init__(self, error, message, source=None, base_exception=None):
        """Utility config custom exception constructor.

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
    """Custom exception class utility config generic exceptions."""

    def __init__(self, base_exception=None):
        """Initialize a UtilityGenericError instance.

        Args:
            base_exception (obj): An exception object.
        """
        caller_frame = inspect.currentframe().f_back
        source = ExceptionSource().get_source(caller_frame)
        super().__init__(
            ("UC-101", "GENERIC_ERROR", HTTPStatus.INTERNAL_SERVER_ERROR),
            "Encounter some internal error. Please contact administrator.",
            source,
            base_exception
        )


class UtilityConfgiRequiredKeyError(UtilityError):
    """Custom exception class utility config required key exceptions."""

    def __init__(self):
        """Initialize a UtilityConfgiRequiredKeyError instance."""
        caller_frame = inspect.currentframe().f_back
        source = ExceptionSource().get_source(caller_frame)
        super().__init__(
            ("UC-102", "UTILITY_CINFIG_REQUIRED_KEY_ERROR",
             HTTPStatus.BAD_REQUEST),
            "The required parameter 'KEY' is missing. Please provide the"
            " 'KEY' parameter.",
            source
        )


class UtilityConfgiTooArgumentsError(UtilityError):
    """Custom exception class utility config too many arguments exceptions."""

    def __init__(self):
        """Initialize a UtilityConfgiTooArgumentsError instance."""
        caller_frame = inspect.currentframe().f_back
        source = ExceptionSource().get_source(caller_frame)
        super().__init__(
            ("UC-103", "UTILITY_CINFIG_TOO_ARGUMENTS_KEY_ERROR",
             HTTPStatus.BAD_REQUEST),
            "GET method accepts two parameters, but more than two were found.",
            source
        )


class UtilityConfigFileNotFoundError(UtilityError):
    """Custom exception class utility config file not found exceptions."""

    def __init__(self):
        """Initialize a UtilityConfigFileNotFoundError instance."""
        caller_frame = inspect.currentframe().f_back
        source = ExceptionSource().get_source(caller_frame)
        super().__init__(
            ("UC-104", "UTILITY_CONFIGE_FILE_NOT_FOUND_ERROR",
             HTTPStatus.BAD_REQUEST),
            "Please ensure that the utility config file exists and the path"
            " is correct.",
            source=source
        )


class UtilityConfigFileENVError(UtilityError):
    """Custom exception class utility config file env exceptions."""

    def __init__(self):
        """Initialize a UtilityConfigFileENVError instance."""
        caller_frame = inspect.currentframe().f_back
        source = ExceptionSource().get_source(caller_frame)
        super().__init__(
            ("UC-105", "UTILITY_CONFIGE_FILE_ENV_NOT_FOUND_ERROR",
             HTTPStatus.BAD_REQUEST),
            "Please ensure that the 'APP_CONFIGURATION_FILE' environment"
            " variable is exported.",
            source=source
        )


class UtilityConfigKeyNotExistsError(UtilityError):
    """Custom exception class utility config file env exceptions."""

    def __init__(self, key):
        """Initialize a UtilityConfigKeyNotExistsError instance."""
        caller_frame = inspect.currentframe().f_back
        source = ExceptionSource().get_source(caller_frame)
        super().__init__(
            ("UC-106", "UTILITY_CONFIGE_KEY_NOT_EXISTS_ERROR",
             HTTPStatus.BAD_REQUEST),
            f"Provided key '{key}' doesn't exists in app configuration file.",
            source=source
        )
