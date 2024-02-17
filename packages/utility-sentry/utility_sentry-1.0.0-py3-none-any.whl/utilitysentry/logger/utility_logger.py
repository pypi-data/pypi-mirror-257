"""This module provide logging functionality.

This module provides a UtilityLogger class that allows for customizable
logging in Python programs. It also imports necessary modules and sets up a
basic logging configuration.

This have the following classes:
    - `UtilityLogger` : This class is responsible for custom logger.
"""
import os
import sys
import logging
import yaml
import inspect
from datetime import datetime
from yaml.loader import SafeLoader
from utilitysentry.comman import constants as cons
from utilitysentry.exception.utility_exception import UtilityException
from utilitysentry.comman.utility_default_logger import UtilityDefaultLogger
from utilitysentry.logger.logger_exception import (
    UtilityGenericError,
    LoggerConfigFileNotFoundError
)

logging.basicConfig(level=logging.ERROR, format=cons.LOGGER_DEFAULT_FORMAT)


class UtilityLogger:
    """This class provide custom logger.

    This class provides a custom logger with configurable log levels and
    handlers. It is designed to simplify logging in Python programs.

    Attributes:
        logger: The logger object associated with the class.
        log_level_name: A dictionary that maps log level names to their
            corresponding values in the logging module.

    Methods:
        __new__(root_log_name="utilitysentry"): Initializes a new instance of
            the UtilityLogger class.
        get_logger(): Gets the logger object of the class.
        initialize_logger(): Initializes the logger object for the
            UtilityLogger class.
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
    _LOGGER_FILE_DEFULT_PATH = "utility-config.yaml"
    _CONFIG_FILE_FOLDER = cons.UTILITY_SENTRY_DEFAULT_FOLDER

    def __new__(cls, root_name="utilitysentry"):
        """Create a new instance of the UtilityLogger class.

        This method is called before the object is created and is responsible
        for creating and initializing the instance variables.

        Args:
            root_log_name (str): A string that represents the root log name.

        Returns:
            instance (object): An instance of the UtilityLogger class.
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(UtilityLogger, cls).__new__(cls)

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
    def initialize_logger(cls):
        """Initialize the logger object for the UtilityLogger class.

        This method sets up the logger configuration with the specified formate
        level, console and file handler.
        """
        try:
            # Creating complete file path of config file.
            file_path = os.path.abspath(os.path.join(
                cls._CONFIG_FILE_FOLDER, cls._LOGGER_FILE_DEFULT_PATH))

            # Checking logger config file path exists or not.
            if not os.path.exists(file_path):
                cls.logger.info("""If file path not exists then raising
                exception""")
                print("\nThe provided file path doesn't exist. Please create"
                      f" an '{cls._CONFIG_FILE_FOLDER}' folder, and within"
                      f" that folder, create the '{cls._CONFIG_FILE_FOLDER}"
                      f"{cls._LOGGER_FILE_DEFULT_PATH}' file.")
                raise LoggerConfigFileNotFoundError()

            try:
                # reading config file
                with open(file_path) as f:
                    config_data = yaml.load(f, Loader=SafeLoader)
            except Exception as e:
                raise UtilityGenericError(e)

            # get log level
            log_level = config_data[cons.DEFAULT_LOG_LEVEL]

            # Setting default log level and formate.
            default_log_formate = config_data[cons.DEFAULT_FORMAT]
            cls.logger.setLevel(cls.log_level_name[log_level])

            # Setting up default handler
            default_formatter = logging.Formatter(default_log_formate)
            default_handler = logging.StreamHandler(sys.stdout)
            cls.logger.addHandler(default_handler)
            default_handler.setFormatter(default_formatter)

            # Setting log handlers based on config file data.
            if cons.HANDLERS in config_data.keys():
                cls.set_log_handler(config_data)

            """To make sure that child logger does not propagate its message to
            the root logger."""
            cls.logger.propagate = False

            # Setting initialized logger to default logger.
            UtilityDefaultLogger.set_logger(cls.logger)
        except UtilityException as e:
            cls.logger.error(e)
            raise e
        except Exception as e:
            cls.logger.error(e)
            raise UtilityGenericError(e)

    @classmethod
    def set_log_handler(cls, config_data):
        """Set logger handlers.

        This method will help us to set logger handlers based on config data.

        Args:
            config_data (dict): A dictionary represents the log config data.
        """
        try:
            # Clearing existing handlers before initializing new handler.
            # Otherwise this will print multiple logs.
            cls.logger.handlers.clear()

            # Creating file handler for logger
            if cons.FILE_HANDLER in config_data[cons.HANDLERS].keys():
                file_config = config_data[cons.HANDLERS][cons.FILE_HANDLER]
                file_path = file_config[
                    cons.LOG_FILE_PATH].format(datetime.now())
                log_folder_path = os.path.dirname(file_path)
                cls._create_log_folder(log_folder_path)

                file_handler = logging.FileHandler(file_path)
                if cons.FORMAT in file_config.keys():
                    file_format = logging.Formatter(
                        file_config[cons.FORMAT]
                    )
                    file_handler.setFormatter(file_format)
                if cons.LOG_LEVEL in file_config.keys():
                    file_handler.setLevel(file_config[cons.LOG_LEVEL])
                cls.logger.addHandler(file_handler)

            # Creating console handler for logger
            if cons.CONSOLE_HANDLER in config_data[cons.HANDLERS].keys():
                console_config = config_data[
                    cons.HANDLERS][cons.CONSOLE_HANDLER]
                console_handler = logging.StreamHandler(sys.stdout)

                if cons.FORMAT in console_config.keys():
                    console_format = logging.Formatter(
                        console_config[cons.FORMAT]
                    )
                    console_handler.setFormatter(console_format)

                if cons.LOG_LEVEL in console_config.keys():
                    console_handler.setLevel(console_config[cons.LOG_LEVEL])

                cls.logger.addHandler(console_handler)
        except UtilityException as e:
            cls.logger.error(e)
            raise e
        except Exception as e:
            cls.logger.error(e)
            raise UtilityGenericError(e)

    @classmethod
    def _create_log_folder(cls, log_folder_path):
        """Create log folder for storing log files.

        This class method checks if the log folder exists at the root
        directory.If the folder does not exist, it will be created.

        Args:
            log_folder_path (str): A string that represents logs file path.
        """
        folder_path = os.path.abspath(log_folder_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

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
