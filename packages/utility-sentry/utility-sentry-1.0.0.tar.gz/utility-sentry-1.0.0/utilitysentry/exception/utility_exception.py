"""This module contain the code for custom exceptions.

This have the following classes:
    - `UtilityException` : This class is responsible for custom exception.
    - `ExceptionSource` : This class is responsible for custom source
        exception.
"""

import traceback
import inspect
from utilitysentry.comman.utility_default_logger import UtilityDefaultLogger


class ExceptionSource:
    """This class contains exception source information.

    This class is used to capture and provide information about the source of
    an exception. It allows you to retrieve the class name, method name, and
    file name from which an exception was raised.
    """

    def __init__(self):
        """Initialize a ExceptionSource class instance."""
        self.caller_frame = inspect.currentframe().f_back
        self.log = UtilityDefaultLogger().get_logger()

    def get_source(self, caller_frame=None):
        """Retrieve information about the calling function.

        This function is used to generate information about the source of an
        exception or to inspect the calling context. this information will
        contains class name, method name, and file location.

        Args:
            caller_frame (object): The frame object of the calling function.

        Returns:
            result (str): A formatted string containing information about the
                calling function.
        """
        try:
            caller_frame = caller_frame if caller_frame else self.caller_frame

            self.log.info("Get the class name (if applicable)")
            classname = None
            if 'self' in caller_frame.f_locals:
                self.log.info("Getting instance method class name.")
                classname = caller_frame.f_locals['self'].__class__.__name__

            if 'cls' in caller_frame.f_locals:
                self.log.info("Getting class method class name.")
                classname = caller_frame.f_locals['cls'].__name__

            self.log.info("Get the method name")
            method = caller_frame.f_code.co_name
            if method == "<module>":
                method = None

            self.log.info("Get the file location")
            location = caller_frame.f_code.co_filename

            self.log.info("Get the location line number.")
            line_number = caller_frame.f_lineno

            result = self.get_source_message(
                classname, method, location, line_number)
            return result
        except Exception as e:
            self.log.error(e)
            return None

    def get_source_message(self, classname, methodname, filename, line_number):
        """Return information about the source of an exception.

        Args:
            classname (str): The name of the class where the exception
                occurred.
            methodname (str): The name of the method where the exception
                occurred.
            filename (str): The file location (path) where the exception
                occurred.
            line_number (int): The line number in the source file where the
                exception occurred.

        Returns:
            source_msg (str): A formatted string containing information about
                the source of the exception.
        """
        source_msg = f"File Path : {filename}"

        if classname:
            classmsg = f"Class : {classname}"
            source_msg += ", " + classmsg if source_msg else classmsg

        if methodname:
            methodmsg = f"Method : {methodname}"
            source_msg += ", " + methodmsg if source_msg else methodmsg

        if line_number:
            linemsg = f"Line No. : {line_number}"
            source_msg += ", " + linemsg if source_msg else linemsg
        return source_msg


class UtilityException(Exception):
    """This class contains Custom exception.

    This class acts as a base class for custom exception.
    It will provide some standard methods for exception.
    """

    def __init__(self, error, message=None, source=None,
                 base_exception=None):
        """Initialize a UtilityException class instance.

        This Method is used for initializing instance variable.

        Args:
            error (object): An object that contains error object information.
            message (string): A string that represents error message.
            source (str): A string that represents exception source location.
            base_exception (obj): An exception object that represents original
                exception.
        """
        self.error_code = error[0]
        self.message_code = error[1]
        self.status_code = error[2]
        self.message = message
        self.base_exception = base_exception
        self.base_exception_message = self.get_original_exception_msg()

        self.stacktrace_printed = False

        # Getting exception source location
        if not source:
            caller_frame = inspect.currentframe().f_back
            source = ExceptionSource().get_source(caller_frame)
        self.source = source

        # Print stacktrace
        self.print_stacktrace()

    def get_original_exception_msg(self):
        """Return original error message.

        Returns:
            error_message (str): Original error message.
        """
        if self.base_exception:
            error_message = repr(self.base_exception)
            return error_message
        return None

    def print_stacktrace(self):
        """Return the complete traceback of an exception and set the\
        stacktrace flag to True.

        Returns:
            Traceback (str): Exception traceback.
        """
        if not self.stacktrace_printed:
            self.stacktrace_printed = True
            exception = self.base_exception if self.base_exception\
                else self

            # Printing exception source and exception.
            print("\n")
            traceback.print_exception(
                type(exception), exception, exception.__traceback__)
            if self.source:
                print(self.source)
            if self.message:
                print(f"{self.message_code}: {self.message}")
