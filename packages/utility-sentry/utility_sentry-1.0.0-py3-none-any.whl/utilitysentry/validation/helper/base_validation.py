"""This module contain all the base methods for utility validation component.

This module contains following classes:
    - `BaseValidator`:- This class is responsible for validator common methods.
"""
import re
from uuid import UUID
from datetime import datetime
from abc import ABC, abstractmethod
from utilitysentry import UtilityException
from utilitysentry.comman import constants as cons
from typing import Optional, List, Tuple, Type
from utilitysentry.comman.utility_default_logger import UtilityDefaultLogger
from utilitysentry.validation.helper import validation_message
from utilitysentry.validation.helper.validation_helper import ValidationHelper
from utilitysentry.validation.validation_exception import (
    UtilityGenericError,
    UtilityValidationFailError,
    UtilityValidationInitializationError
)


class BaseValidator(ABC):
    """This class provide helper methods for utility validation component."""

    RANGE_PARAM_LENGTH = 2

    def __init__(self,
                 required: bool = False,
                 max_length: Optional[int] = None,
                 min_length: Optional[int] = None,
                 range: Optional[Tuple] = None,
                 item: Optional[str] = None,
                 validation: Optional[Type] = None,
                 choices: Optional[List] = None,
                 unique: bool = False,
                 date_format: Optional[str] = None,
                 regex: Optional[str] = None,
                 allow_special_characters: bool = True):
        """Initialize a BaseValidator class instance."""
        self.log = UtilityDefaultLogger().get_logger()
        self._validate_parameters_datatype(
            required=required,
            max_length=max_length,
            min_length=min_length,
            choices=choices,
            range=range,
            unique=unique,
            date_format=date_format,
            item=item,
            regex=regex,
            allow_special_characters=allow_special_characters,
            validation=validation
        )
        self.required = required
        self.max_length = max_length
        self.min_length = min_length
        self.choices = choices
        self.range = range
        self.unique = unique
        self.date_format = date_format
        self.item = item
        self.regex = regex
        self.allow_special_characters = allow_special_characters
        self.validation = validation

    def _validate_parameters_datatype(self, **kwargs):
        """Validate parameters datatype using the ValidationHelper."""
        try:
            self.log.info("Validating required parameter.")
            ValidationHelper.validate_bool(
                cons.REQUIRED, kwargs[cons.REQUIRED])

            self.log.info("Validating max length parameter.")
            ValidationHelper.validate_optional_int(
                cons.MAX_LENGTH, kwargs[cons.MAX_LENGTH])

            self.log.info("Validating min length parameter.")
            ValidationHelper.validate_optional_int(
                cons.MIN_LENGTH, kwargs[cons.MIN_LENGTH])

            self.log.info("Validating choices parameter.")
            ValidationHelper.validate_optional_list(
                cons.CHOICES, kwargs[cons.CHOICES])

            self.log.info("Validating range parameter.")
            ValidationHelper.validate_optional_tuple(
                cons.RANGE, kwargs[cons.RANGE])
            ValidationHelper.validate_optional_length(
                self.RANGE_PARAM_LENGTH, cons.RANGE, kwargs[cons.RANGE])

            self.log.info("Validating unique parameter.")
            ValidationHelper.validate_bool(cons.UNIQUE, kwargs[cons.UNIQUE])

            self.log.info("Validating date format parameter.")
            ValidationHelper.validate_str_or_none(
                cons.DATE_FORMAT, kwargs[cons.DATE_FORMAT])

            self.log.info("Validating item parameter.")
            ValidationHelper.validate_str_or_none(cons.ITEM, kwargs[cons.ITEM])
            ValidationHelper.validate_item_param(cons.ITEM, kwargs[cons.ITEM])

            self.log.info("Validating regex parameter.")
            ValidationHelper.validate_str_or_none(
                cons.REGEX, kwargs[cons.REGEX])

            self.log.info("Validating allow special characters parameter.")
            ValidationHelper.validate_bool(
                cons.ALLOW_SPECIAL_CHARACTERS,
                kwargs[cons.ALLOW_SPECIAL_CHARACTERS])

            self.log.info("Validating allow special characters parameter.")
            ValidationHelper.validate_validation_param(
                cons.VALIDATION, kwargs[cons.VALIDATION])
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def _validate_accepted_parameters(
            self, class_name, accepted_params, input_params):
        """Validate the provided parameters against accepted parameters.

        This method validates whether the keys of the provided parameters
        dictionary exist in the accepted parameters list. If any key in the
        provided parameters dictionary does not exist in the accepted
        parameters list, it raises an exception.

        Args:
            class_name (str): A class name of current validation class.
            accepted_params (list): A list of accepted parameter names.
            input_params (dict): A dictionary containing the provided
                parameters.

        Raises:
            UtilityValidationFailError: If any key in input_params does not
                exist in accepted_params.
        """
        try:
            self.log.info("Validating accepted parameters parameter.")
            for key in input_params.keys():
                if key not in accepted_params:
                    message = validation_message.ACCEPTED_PARAMS_FAIL_ERROR
                    message = message.format(class_name, accepted_params)
                    raise UtilityValidationInitializationError(message)
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    @abstractmethod
    def validate(self, key, params):
        """Abstract method class to extend and override based on their needs.

        Args:
            key (str): The key or name of the parameter being validated.
            params (dict): A dicstionary value of the parameter to be
                validated.
        """
        pass

    @abstractmethod
    def _validate_init_method_arguments(self, *args, **kwargs):
        """Abstract method class to extend and override based on their needs.

        Args:
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        pass

    def _validate_datatype(self, key, data):
        """Validate the 'datatype' of parameter.

        This method checks if the datatype of the parameter matches the
        expected datatype and raises an exception if not.

        Args:
            key (str): The key or name of the parameter being validated.
            value (str): The value of the parameter to be validated.

        Raises:
            UtilityValidationFailError: If the 'datatype' is not as expected.
        """
        try:
            self.log.info(f"Validating 'datatype' for {key}.")
            if not isinstance(data, self.DATA_TPYE):
                self.log.info("If Validation fail then raise Exception.")
                message = validation_message.DATATYPE_VALIDATION_FAIL
                message = message.format(key, self.DATA_TYPE_NAME)
                raise UtilityValidationFailError(message)
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def _validate_required(self, key, value):
        """Validate the 'required' parameter.

        This method checks if a required parameter is provided with a non-empty
        value.

        Args:
            key (str): The key or name of the parameter being validated.
            value (str): The value of the parameter to be validated.

        Raises:
            UtilityValidationFailError: If the 'required' flag is True and the
                provided value is empty.
        """
        try:
            if self.required:
                if value is None:
                    self.log.info("Validating 'required' parameter.")
                    message = validation_message.REQUIRED_VALIDATION_FAIL
                    raise UtilityValidationFailError(message.format(key))
                elif (not isinstance(value, bool) and not value):
                    self.log.info("If Validation fail then raise Exception.")
                    message = validation_message.REQUIRED_VALIDATION_FAIL
                    raise UtilityValidationFailError(message.format(key))
                elif (isinstance(value, str) and value.strip() == ""):
                    self.log.info("""If String Validation fail then raise
                    Exception.""")
                    message = validation_message.REQUIRED_VALIDATION_FAIL
                    raise UtilityValidationFailError(message.format(key))
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def _validate_max_length(self, key, value):
        """Validate the 'max_length' parameter.

        This method checks if the length of the provided value exceeds the
        maximum allowed length.

        Args:
            key (str): The key or name of the parameter being validated.
            value (any): The value of the parameter to be validated.

        Raises:
            UtilityValidationFailError: If 'max_length' is specified and the
                length of the value exceeds the maximum.
        """
        try:
            self.log.info(f"Validating 'max_length'  parameter for {key}.")
            if (value and self.max_length is not None and
                    len(value) > self.max_length):
                self.log.info("If Validation fail then raise Exception.")
                message = validation_message.MAX_LENGTH_VALIDATION_FAIL
                message = message.format(key, self.max_length)
                raise UtilityValidationFailError(message)
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def _validate_min_length(self, key, value):
        """Validate the 'min_length' parameter.

        This method checks if the length of the provided value meets the
        minimum required length.

        Args:
            key (str): The key or name of the parameter being validated.
            value (any): The value of the parameter to be validated.

        Raises:
            UtilityValidationFailError: If 'min_length' is specified and the
                length of the value is less than the minimum required length.
        """
        try:
            self.log.info(f"Validating 'min_length' parameter for {key}.")
            if (value and self.min_length is not None and
                    len(value) < self.min_length):
                self.log.info("If validation fails, raise Exception.")
                message = validation_message.MIN_LENGTH_VALIDATION_FAIL
                message = message.format(key, self.min_length)
                raise UtilityValidationFailError(message)
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def _validate_choices(self, key, value):
        """Validate the 'choices' parameter.

        This method checks if the provided value matches the specified choices.

        Args:
            key (str): The key or name of the parameter being validated.
            value (any): The value of the parameter to be validated.

        Raises:
            UtilityValidationFailError: If 'choices' is specified and the
                value does not match the allowed choices.
        """
        try:
            self.log.info(f"Validating 'choices' parameter for {key}.")
            if (value and self.choices is not None and
                    value not in self.choices):
                self.log.info("If validation fails, raise Exception.")
                message = validation_message.CHOICES_VALIDATION_FAIL
                message = message.format(key, self.choices)
                raise UtilityValidationFailError(message)
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def _validate_range(self, key, value):
        """Validate the 'range' parameter.

        This method checks if the provided value is within the specified range.

        Args:
            key (str): The key or name of the parameter being validated.
            value (int): The value of the parameter to be validated.

        Raises:
            UtilityValidationFailError: If 'range' is specified and the
                value is outside the specified range.
        """
        try:
            self.log.info(f"Validating 'range' parameter for {key}.")
            if (value and self.range is not None and not (
                    self.range[0] <= value <= self.range[1])):
                self.log.info("If validation fails, raise Exception.")
                message = validation_message.RANGE_VALIDATION_FAIL
                message = message.format(key, self.range)
                raise UtilityValidationFailError(message)
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def _validate_unique(self, key, value):
        """Validate the 'unique' parameter.

        This method checks if the provided list, set, tuple should be unique.

        Args:
            key (str): The key or name of the parameter being validated.
            value (any): The value of the parameter to be validated.

        Raises:
            UtilityValidationFailError: If 'unique' is specified and the
                value contains duplicate values.
        """
        try:
            self.log.info(f"Validating 'unique' parameter for {key}.")
            if self.unique and value:
                self.log.info("Checking for duplicate values.")
                if len(value) != len(set(value)):
                    self.log.info("If validation fails, raise Exception.")
                    duplicate_values = [
                        item for item in value if value.count(item) > 1]
                    message = validation_message.UNIQUE_VALIDATION_FAIL
                    message = message.format(key, duplicate_values)
                    raise UtilityValidationFailError(message)
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def _validate_date_format(self, key, value):
        """Validate the 'date_format' parameter.

        This method checks if the provided date format matches the specified
        format.

        Args:
            key (str): The key or name of the parameter being validated.
            value (str): The value of the parameter to be validated.

        Raises:
            UtilityValidationFailError: If 'date_format' is specified and the
                format doesn't match.
        """
        try:
            self.log.info(f"Validating 'date_format' parameter for {key}.")
            if self.date_format is not None and value:
                self.log.info("Checking date format")
                try:
                    datetime.strptime(value, self.date_format)
                except Exception:
                    message = validation_message.DATE_FORMAT_VALIDATION_FAIL
                    message = message.format(key, self.date_format)
                    raise UtilityValidationFailError(message)
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def _validate_item(self, key, value):
        """Validate the 'item' parameter.

        This method checks if each item in the list matches the specified data
        type.

        Args:
            key (str): The key or name of the parameter being validated.
            value (list): The list to be validated.

        Raises:
            UtilityValidationFailError: If any item in the list does not match
                the specified data type.
        """
        try:
            self.log.info(f"Validating 'item' parameter for {key}.")
            if self.item and value:
                self.log.info(
                    f"Checking data type of each item in the list for {key}.")
                data_type = cons.DATA_TYPE_LIST[self.item.lower()]
                for item in value:
                    if not isinstance(item, data_type):
                        message = validation_message.ITEM_VALIDATION_FAIL
                        message = message.format(key, self.item)
                        raise UtilityValidationFailError(message)
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def _validate_regex(self, key, value):
        """Validate the 'regex' parameter.

        This method checks if the provided value matches the specified regex
        pattern.

        Args:
            key (str): The key or name of the parameter being validated.
            value (str): The value to be validated.

        Raises:
            UtilityValidationFailError: If the value does not match the regex
                pattern.
        """
        try:
            self.log.info(f"Validating 'regex' parameter for {key}.")
            if self.regex and value:
                self.log.info("Checking regex pattern")
                if not re.match(self.regex, value):
                    message = validation_message.REGEX_VALIDATION_FAIL
                    message = message.format(key, self.regex)
                    raise UtilityValidationFailError(message)
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def _validate_allow_special_characters(self, key, value):
        """Validate the 'allow_special_characters' parameter.

        This method checks if special characters are allowed in the provided
        value.

        Args:
            key (str): The key or name of the parameter being validated.
            value (str): The value of the parameter to be validated.

        Raises:
            UtilityValidationFailError: If 'allow_special_characters' is False
                and the value contains special characters.
        """
        try:
            self.log.info(f"""Validating 'allow_special_characters' parameter
            for {key}.""")
            if not self.allow_special_characters and not value.isalnum():
                self.log.info("If validation fails, raise Exception.")
                message = validation_message.SPECIAL_CHARACTERS_VALIDATION_FAIL
                message = message.format(key)
                raise UtilityValidationFailError(message)
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def _validate_additional_validation(self, key, value):
        """Validate the nested dictionary.

        This method helps to validate nested dictionary objects.

        Args:
            key (str): The key or name of the parameter being validated.
            value (dict): The value of the parameter to be validated.

        Raises:
            UtilityValidationFailError: If validation fails for the nested
                dictionary.
        """
        try:
            self.log.info(f"""Validating 'validation' parameter for {key}.""")
            if self.validation is not None:
                from utilitysentry.validation import UtilityValidator
                self.log.info("Check if it's a class or an object")
                if isinstance(self.validation, type):
                    validation_instance = self.validation()
                elif isinstance(self.validation, UtilityValidator):
                    validation_instance = self.validation

                validation_instance.validate(value)
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def _validate_uuid(self, key, value):
        """Validate the UUID parameter or value.

        This method checks if the provided value is a valid UUID string and
        returns True if it is otherwise False.

        Args:
            key (str): The key or name of the parameter being validated.
            value (str): The value of the parameter to be validated.

        Raises:
            UtilityValidationFailError: If the value is not a valid UUID.
        """
        self.log.info("Validating UUID parameter.")
        try:
            try:
                UUID(str(value))
            except ValueError:
                message = validation_message.UUID_VALIDATION_FAIL
                message = message.format(key)
                raise UtilityValidationFailError(message)
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def _validate_item_uuid(self, key, value):
        """Validate UUID item.

        This method validates UUID item.

        Args:
            key (str): The key or name of the parameter being validated.
            value (dict): A value of the parameter to be validated.

        Raises:
            UtilityValidationFailError: If any of the validation checks fail.
        """
        try:
            self.log.info("Validating UUID item.")
            for data in value:
                self._validate_uuid(key, data)
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def _validate_item_date_format(self, key, value):
        """Validate item date format.

        This method validates the date format of each item in the given value.

        Args:
            key (str): The key or name of the parameter being validated.
            value (dict): A value of the parameter to be validated.

        Raises:
            UtilityValidationFailError: If any of the validation checks fail.
        """
        try:
            self.log.info("Validating item date format.")
            if not self.date_format:
                mesaage = validation_message.ITEM_DATETIME_INITIALIZE_FAIL
                raise UtilityValidationInitializationError(mesaage)
            for data in value:
                self._validate_date_format(key, data)
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)

    def _validate_item_utility_validation(self, key, value):
        """Validate the nested dictionary.

        This method helps to validate each nested dictionary objects of
        provided lists of dictionaries.

        Args:
            key (str): The key or name of the parameter being validated.
            value (dict): A value of the parameter to be validated.

        Raises:
            UtilityValidationFailError: If any of the validation checks fail.
        """
        try:
            self.log.info("Validating additional validation.")
            if not self.validation:
                mesaage = validation_message.ITEM_UTILITY_INITIALIZE_FAIL
                raise UtilityValidationInitializationError(mesaage)

            for data in value:
                self._validate_additional_validation(key, data)
        except UtilityException as e:
            self.log.error(e)
            raise e
        except Exception as e:
            self.log.error(e)
            raise UtilityGenericError(e)
