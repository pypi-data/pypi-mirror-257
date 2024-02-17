"""This module provides functionality to read configuration files.

This module includes a `UtilityConfig` class that facilitates the reading
of configuration files based on environment variables and allows retrieval
of values for provided keys.

This have the following classes:
    - `UtilityConfig` : Responsible for reading configuration files.
"""
import os
import yaml
from utilitysentry import UtilityException
from utilitysentry.comman import constants as cons
from utilitysentry.comman.utility_default_logger import UtilityDefaultLogger
from utilitysentry.config.config_exception import (
    UtilityGenericError,
    UtilityConfgiRequiredKeyError,
    UtilityConfgiTooArgumentsError,
    UtilityConfigFileNotFoundError,
    UtilityConfigFileENVError,
    UtilityConfigKeyNotExistsError
)


class UtilityConfig:
    """A utility class for reading configuration files.

    The `UtilityConfig` class provides methods to load configuration files
    based on an environment variable. It follows the singleton pattern to
    ensure that only one instance of the configuration is loaded.
    Additionally, it allows for the retrieval of configuration values and
    provides default values when necessary.
    """
    _instance = None
    _DEFAULT_PARAM_KEY = "default"
    _FILE_PATH_ENV = "APP_CONFIGURATION_FILE"
    _CONFIG_FILE_FOLDER = cons.UTILITY_SENTRY_DEFAULT_FOLDER

    def __new__(cls):
        """Create a new instance of the UtilityConfig class.

        This method is called before the object is created and is responsible
        for creating and initializing the instance variables.

        Returns:
            instance (object): An instance of the UtilityConfig class.
        """
        if not cls._instance:
            cls._instance = super(UtilityConfig, cls).__new__(cls)
            cls._instance._config_data = None
        return cls._instance

    def __init__(self):
        """Initialize a UtilityConfig instance."""
        self.log = UtilityDefaultLogger().get_logger()
        self._config_file_path = None

    def _get_config_file_path(self):
        """Get app configuration file path.

        This method will help us to get app configuration file path and help us
        to check that file exists or not.

        Returns:
            file_path (str): A string that represents configuration file path.
        """
        try:
            file_name = os.getenv(self._FILE_PATH_ENV)
            if not file_name:
                self.log.info("If file_name is none then raising exception.")
                raise UtilityConfigFileENVError()

            self.log.info("Creating complete file path of config file.")
            file_path = os.path.abspath(os.path.join(
                self._CONFIG_FILE_FOLDER, file_name))

            self.log.info("Checking logger config file path exists or not.")
            if not os.path.exists(file_path):
                self.log.info("If file path not exists then raising exception")
                print("\nThe provided file path doesn't exist. Please create"
                      f" an '{self._CONFIG_FILE_FOLDER}' folder, and within"
                      f" that folder, create the '{self._CONFIG_FILE_FOLDER}"
                      f"{self._FILE_PATH_ENV}' file.")
                raise UtilityConfigFileNotFoundError()

            self._config_file_path = file_path
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def load_config(self):
        """Load configuration data from a YAML file.

        Checks for file existence, handles potential YAML parsing errors,
        and stores the parsed configuration data in the object's `_config_data`
        attribute.
        """
        try:
            if not self._config_data:
                self._get_config_file_path()
                try:
                    with open(self._config_file_path, 'r') as file:
                        self._config_data = yaml.safe_load(file)
                    self.log.info(f"""Config loaded from
                    {self._config_file_path}""")
                except Exception as e:
                    self.log.error(e)
                    raise UtilityGenericError(e)
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def get(self, key, *args, **kwargs):
        """Retrieve a value based on a key, along with an default value.

        Args:
            key (str): The required key to retrieve the value.
            default: Optional default value to return if the key is not found.
                - Can be provided as a positional argument
                    (e.g., "default_value")
                - Can be provided as a keyword argument
                    (e.g., default="default_value")
                - Only one optional argument (either positional or keyword)
                    is allowed.

        Returns:
            value (any): The value associated with the key, or default if not
                found.
        """
        try:
            self.log.info("Checking key is None or Not.")
            if not key:
                self.log.info("If Key is none then raising exception.")
                raise UtilityConfgiRequiredKeyError()

            self.log.info("Checking optional args should be only 1.")
            optional_args_count = len(args) + len(kwargs)
            if optional_args_count > 1:
                self.log.info("""If optional param more then 1 then raising
                exception.""")
                raise UtilityConfgiTooArgumentsError()

            self.log.info("converting project key into string.")
            provided_key = str(key)

            self.log.info("Checking value in environment variable.")
            env_value = os.getenv(provided_key)
            if env_value:
                return env_value

            self.log.info("Loading config data if not loaded.")
            if not self._config_data:
                self.load_config()

            self.log.info("Checking value in '_config_data' variable.")
            if provided_key in self._config_data:
                param_value = self._config_data.get(provided_key)
                return param_value

            if args:
                default_value = args[0]
                return default_value
            elif kwargs:
                if self._DEFAULT_PARAM_KEY in kwargs:
                    default_value = kwargs.get(self._DEFAULT_PARAM_KEY)
                    return default_value
                else:
                    raise UtilityConfigKeyNotExistsError(provided_key)
            else:
                self.log.info("If key value and default value None.")
                raise UtilityConfigKeyNotExistsError(provided_key)
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)
