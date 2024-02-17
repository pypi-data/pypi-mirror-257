"""This module provide functionality to validate float object.

This module provides a UtilityValidator class that allows for validating
a float value of JSON object.

This have the following classes:
    - `Float` : This class is responsible for validating a float object.
"""
from utilitysentry.comman import constants as cons
from utilitysentry import UtilityException
from utilitysentry.validation.helper.base_validation import \
    BaseValidator
from utilitysentry.validation.helper import validation_message
from utilitysentry.validation.utility_validator import UtilityValidator
from utilitysentry.comman.utility_default_logger import UtilityDefaultLogger
from utilitysentry.validation.validation_exception import (
    UtilityGenericError,
    UtilityValidationInitializationError
)


class Float(BaseValidator, UtilityValidator):
    """Validate a Float object.

    This class provide functionality to validate a Float object. It is
    designed to simplify validation operations in Python programs.
    """

    DATA_TPYE = float
    DATA_TYPE_NAME = "Float"
    CLASS_NAME = "Float"

    def __init__(self, *args, **kwargs):
        """Initialize a Float class instance."""
        self.log = UtilityDefaultLogger().get_logger()
        self._validate_init_method_arguments(*args, **kwargs)
        super(Float, self).__init__(**kwargs)

    def _validate_init_method_arguments(self, *args, **kwargs):
        """Validate the arguments of the initialization method.

        This method validates the arguments of the initialization method,
        checking for supported and unsupported arguments. It also ensures
        that positional arguments are not allowed.

        Raises:
            UtilityValidationInitializationError: If the initialization is not
                as expected.
        """
        try:
            self.log.info("Validating positional arguments.")
            if args:
                raise UtilityValidationInitializationError(
                    validation_message.ARGS_NOT_SUPPORT)

            self.log.info("Validating acceptable arguments.")
            self._validate_accepted_parameters(
                self.CLASS_NAME, cons.FLOAT_CLASS, kwargs)

        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def validate(self, key, value):
        """Validate parameter for Float class.

        This method validates the input parameters for the Float class.

        Args:
            key (str): The key or name of the parameter being validated.
            value (dict): A value of the parameter to be validated.

        Returns:
            result (dict): A dictionary that represents provided key, value
                response.

        Raises:
            UtilityValidationFailError: If any of the validation checks fail.
        """
        try:
            self.log.info("Validating required check.")
            self._validate_required(key, value)

            self.log.info("Validating datatype check.")
            if value is not None:
                self._validate_datatype(key, value)

            self._validate_choices(key, value)
            self._validate_range(key, value)

            self.log.info("Creating Object.")
            result = {key: value}
            return result
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)
