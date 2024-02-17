"""This module provide logging functionality for utility sentry.

This module provides a UtilityDefaultLogger class that allows for customizable
logging in Python programs. It also imports necessary modules and sets up a
basic logging configuration.

This have the following classes:
    - `UtilityDefaultLogger` : This class is responsible for custom logger.
"""
import logging
import inspect
from utilitysentry.comman import constants as cons

logging.basicConfig(level=logging.ERROR, format=cons.LOGGER_DEFAULT_FORMAT)


class UtilityDefaultLogger:
    """This class provide custom logger.

    This class provides a custom logger with configurable log levels and
    handlers. It is designed to simplify logging in Python programs.

    Attributes:
        logger: The logger object associated with the class.
        log_level_name: A dictionary that maps log level names to their
            corresponding values in the logging module.

    Methods:
        __new__(root_log_name="utilitysentry"): Initializes a new instance of
            the UtilityDefaultLogger class.
        get_logger(): Gets the logger object of the class.
        initialize_logger(): Initializes the logger object for the
            UtilityDefaultLogger class.
        set_log_handler(config_data): Sets logger handlers based on
            config data.
        update_level(level, handler): Updates logger level at runtime.
    """

    logger = None
    log_level_name = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    def __new__(cls, root_name="utilitysentry"):
        """Create a new instance of the UtilityDefaultLogger class.

        This method is called before the object is created and is responsible
        for creating and initializing the instance variables.

        Args:
            root_log_name (str): A string that represents the root log name.

        Returns:
            instance (object): An instance of the UtilityDefaultLogger class.
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(UtilityDefaultLogger, cls).__new__(cls)

        if not cls.logger:
            cls.logger = logging.getLogger(root_name)
        return cls.instance

    @classmethod
    def get_logger(cls):
        """Get the logger object of the class.

        If logger_name is None then it will return root looger

        Args:
            logger_name (str): A string represents the logger name.

        Returns:
            logger (object): The logger object associated with the class.
        """
        caller_frame = inspect.currentframe().f_back
        logger_name = cls.get_class_name(caller_frame)
        if not logger_name:
            return cls.logger
        return cls.logger.getChild(logger_name)

    @classmethod
    def set_logger(cls, logger):
        """Set the logger object for the class.

        This class method sets the logger object for the class. The logger
        object can be used for logging purposes within the class or its
        methods.

        Args:
            logger (object): The logger object to be set. Defaults to None.
        """
        if isinstance(logger, logging.Logger):
            log_level = logger.getEffectiveLevel()
            if log_level >= cls.log_level_name["ERROR"]:
                cls.logger = logger

    @classmethod
    def get_class_name(cls, caller_frame):
        """Get logger classname.

        This method will return class name to get child logger.

        Args:
            caller_frame (object): The frame object of the calling function.

        Returns:
            logger_name (str): A string represents the logger name.
        """
        cls.logger.info("Get the class name (if applicable)")
        classname = None
        if 'self' in caller_frame.f_locals:
            cls.logger.info("Getting instance method class name.")
            classname = caller_frame.f_locals['self'].__class__.__name__

        if 'cls' in caller_frame.f_locals:
            cls.logger.info("Getting class method class name.")
            classname = caller_frame.f_locals['cls'].__name__

        if classname:
            return str(classname)

        return classname
