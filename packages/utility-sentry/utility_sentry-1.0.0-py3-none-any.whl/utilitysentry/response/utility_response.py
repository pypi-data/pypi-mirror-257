"""Utility response class.

This module defines to create success and error response for your django
application.

Classes:
    - `UtilityResponse`: This class is responsible for API response creation.
"""
import inspect
from http import HTTPStatus
from utilitysentry import UtilityException, ExceptionSource
from utilitysentry.comman import constants as cons


class UtilityResponse:
    """This class to create success and error response.

    UtilityResponse class provide functionality to create success and error
    response for your django application.
    """

    def success_response(self, data, message, extra_dict=None):
        """Get success response.

        The success_response function is used to return a success
        response with the given data, message_code and status_code.

        Args:
            data (dict): The data that is to be returned in the response.
            message (str): A string that represents the success message.
            extra_dict (dict): Add extra information into the response.

        Returns:
            response (object): An HTTP response object.
        """
        response_format = {}
        response_format[cons.STATUS] = cons.SUCCESS_STATUS
        response_format[cons.MESSAGE] = message
        response_format[cons.SUCCESS_RESPONSE_KEY] = data

        if extra_dict:
            response_format.update(extra_dict)
        return response_format

    def error_response(self, exception, message=None):
        """Get error response.

        The error_response function creates a JSON response.

        Args:
            exception (obj): An Exception object.
            message (string): A string that represents error message.

        Returns:
            response (object): An HTTP response object.
        """
        response_format = {}
        response_format[cons.STATUS] = cons.ERROR_STATUS

        if message:
            self.GENERIC_ERROR_MSG = message

        caller_frame = inspect.currentframe().f_back
        source = ExceptionSource().get_source(caller_frame)
        exception = self.get_exception(exception, source)

        error_response_dict = {
            cons.ERROR_CODE: exception.error_code,
            cons.ERROR_MESSAGE_CODE: exception.message_code,
            cons.ERROR_MESSAGE: exception.message,
            cons.ERROR_BASE_EXP_MESSAGE: exception.base_exception_message,
            cons.ERROR_SOURCE: exception.source
        }
        response_format[cons.ERROR_RESPONSE_KEY] = error_response_dict
        return response_format

    def get_exception(self, exception, source):
        """Get exception object.

        This method will help us to get exception object, if exception object
        is not a instance of UtilityException then it will create new
        UtilityException object from provided exception object.

        Args:
            exception (obj): An Exception object.
            source (str): A string that represents exception source location.

        Returns:
            exception (obj): An Exception object.
        """
        if (exception.__class__ == UtilityException or
                issubclass(exception.__class__, UtilityException)):
            return exception
        else:
            CODE_500 = HTTPStatus.INTERNAL_SERVER_ERROR
            GENERIC_ERROR = ("UR-101", "GENERIC_ERROR", CODE_500)
            GENERIC_ERROR_MSG = "Encounter some internal error. Please"\
                " contact administrator."
            ce = UtilityException(
                GENERIC_ERROR, message=GENERIC_ERROR_MSG, source=source,
                base_exception=exception)
            return ce
