"""This module provide functionality to validate JSON object.

This module provides a UtilityValidator class that allows for validating
a JSON object.

This have the following classes:
    - `UtilityValidator` : This class is responsible for validating a JSON
        object.
"""
from utilitysentry import UtilityException
from utilitysentry.validation.helper import validation_message
from utilitysentry.comman.utility_default_logger import UtilityDefaultLogger
from utilitysentry.validation.validation_exception import (
    UtilityGenericError,
    UtilityValidationFailError
)


class UtilityValidator:
    """Validate a JSON object.

    This class provide functionality to validate a JSON object. It is designed
    to simplify validation operations in Python programs.
    """

    def __init__(self):
        """Initialize a UtilityConfig instance."""
        self.log = UtilityDefaultLogger().get_logger()

    def validate(self, parameters):
        """Validate provided JSON object.

        This method will help us to validate provided JSON object.

        Args:
            parameters (dict): A dictionary to be validated.

        Returns:
            validated_data (dict): A dictionary that contains validated data.

        Raises:
            UtilityException: If any of the validation checks fail.
        """
        try:
            if parameters and not isinstance(parameters, dict):
                message = validation_message.JSON_VALIDATION_FAIL
                raise UtilityValidationFailError(message)
            self.log.info("Get the class attributes using vars()")
            class_attributes = vars(self.__class__)

            self.log.info("Iterate through the attributes and their values")
            validated_data = {}
            for param, param_value in class_attributes.items():
                if (hasattr(param_value, "__class__") and
                        issubclass(param_value.__class__, UtilityValidator)):
                    value = parameters.get(param)
                    validated_data.update(param_value.validate(param, value))

            return validated_data
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)
