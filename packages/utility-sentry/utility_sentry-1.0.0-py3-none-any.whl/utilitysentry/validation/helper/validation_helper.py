"""This module contain all the helper methods for utility validation component.

This module contains following classes:
    - `ValidationHelper`:- This class is responsible for validator helper
        methods.
"""
from utilitysentry.comman import constants as cons
from utilitysentry.validation.helper import validation_message
from utilitysentry.validation.validation_exception import (
    UtilityValidationInitializationError
)


class ValidationHelper:
    """A helper class for validating parameters of the BaseValidator class.

    This module provides a set of static methods to validate parameters
    for the BaseValidator class's __init__ method.
    """

    @staticmethod
    def validate_bool(key: str, value):
        """Validate a boolean parameter."""
        if not isinstance(value, bool):
            raise UtilityValidationInitializationError(
                validation_message.BOOL_DATATYPE_ERROR.format(key))

    @staticmethod
    def validate_optional_int(key: str, value):
        """Validate an optional integer parameter."""
        if value is not None and not isinstance(value, int):
            raise UtilityValidationInitializationError(
                validation_message.OPTIONAL_INT_DATATYPE_ERROR.format(key))

    @staticmethod
    def validate_optional_list(key: str, value):
        """Validate an optional list parameter."""
        if value is not None and not isinstance(value, list):
            raise UtilityValidationInitializationError(
                validation_message.OPTIONAL_LIST_DATATYPE_ERROR.format(key))

    @staticmethod
    def validate_optional_tuple(key: str, value):
        """Validate an optional tuple parameter."""
        if value is not None and not isinstance(value, tuple):
            raise UtilityValidationInitializationError(
                validation_message.OPTIONAL_TUPLE_DATATYPE_ERROR.format(key))

    @staticmethod
    def validate_str_or_none(key: str, value):
        """Validate a string or None parameter."""
        if value is not None and not isinstance(value, str):
            raise UtilityValidationInitializationError(
                validation_message.STR_OR_NONE_DATATYPE_ERROR.format(key))

    @staticmethod
    def validate_str(key: str, value):
        """Validate a string parameter."""
        if not isinstance(value, str):
            raise UtilityValidationInitializationError(
                validation_message.STR_DATATYPE_ERROR.format(key))

    @staticmethod
    def validate_optional_length(length: int, key: str, value):
        """Validate a tuple length or None parameter."""
        if value is not None and (len(value) != length):
            raise UtilityValidationInitializationError(
                validation_message.LENGTH_ERROR.format(key, length))

    @staticmethod
    def validate_item_param(key, value):
        """Validate a item parameter value or None parameter."""
        if (value is not None and
            (not isinstance(value, str) or
                value.lower() not in cons.DATA_TYPE_LIST.keys())):
            raise UtilityValidationInitializationError(
                validation_message.ITEM_PARAM_INITIALIZATION_FAIL.format(
                    key, list(cons.DATA_TYPE_LIST.keys())))

    @staticmethod
    def validate_validation_param(key, value):
        """Validate a validator parameter value or None parameter."""
        from utilitysentry.validation import UtilityValidator
        if (value is not None and
            not (isinstance(value, UtilityValidator) or
                 issubclass(value, UtilityValidator))):
            raise UtilityValidationInitializationError(
                validation_message.VALIDATION_PARAM_INITIALIZE_FAIL.format(
                    key, UtilityValidator.__name__))
