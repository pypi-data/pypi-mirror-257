"""This module will contains contant values for utility sentry."""
from uuid import UUID
from datetime import datetime

# Contant values of Utility Sentry default folder
UTILITY_SENTRY_DEFAULT_FOLDER = "resource"

# Contant values of default logger component.
LOGGER_DEFAULT_FORMAT = "[%(asctime)s] %(levelname)s"\
    " [%(filename)s:%(lineno)s] %(name)s %(module)s %(funcName)s:- %(message)s"

# Utility response class constant value
STATUS = "status"

SUCCESS_STATUS = "success"
MESSAGE = "message"
SUCCESS_RESPONSE_KEY = "data"

ERROR_STATUS = "error"
ERROR_CODE = "code"
ERROR_MESSAGE = "message"
ERROR_MESSAGE_CODE = "message_code"
ERROR_BASE_EXP_MESSAGE = "base_exception_message"
ERROR_SOURCE = "source"
ERROR_RESPONSE_KEY = "error"

# Utility logger class constant value
DEFAULT_LOG_LEVEL = "default_loglevel"
DEFAULT_FORMAT = "default_format"
HANDLERS = "handlers"
FILE_HANDLER = "file"
CONSOLE_HANDLER = "console"
FORMAT = "format"
LOG_LEVEL = "loglevel"
LOG_FILE_PATH = "filepath"

# Utility validation class constant value
UUID_DATATYPE = "uuid"
DATETIME_DATATYPE = "datetime"
VALIDATION_DATATYPE = "validation"

DATA_TYPE_LIST = {
    "string": str,
    "list": list,
    "dictionary": dict,
    "tuple": tuple,
    "set": set,
    "integer": int,
    "float": float,
    "boolean": bool,
    "nonetype": type(None),
    "bytes": bytes,
    "bytearray": bytearray,
    "complex": complex,
    "uuid": UUID,
    "datetime": datetime,
    "validation": None
}
REQUIRED = "required"
MAX_LENGTH = "max_length"
MIN_LENGTH = "min_length"
CHOICES = "choices"
RANGE = "range"
UNIQUE = "unique"
DATE_FORMAT = "date_format"
ITEM = "item"
REGEX = "regex"
ALLOW_SPECIAL_CHARACTERS = "allow_special_characters"
VALIDATION = "validation"

DEFAULT_PASSWORD_REGEX = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=]).+$'
DEFAULT_EMAIL_REGEX = r'^\w+@\w+\.\w+$'

# Contant value of Utility validation Sub class.
# String validation
STRING_CLASS = [
    REQUIRED, MAX_LENGTH, MIN_LENGTH, CHOICES, REGEX, ALLOW_SPECIAL_CHARACTERS]
IS_NUMERIC_CLASS = [REQUIRED, MAX_LENGTH, MIN_LENGTH, CHOICES, REGEX]

# Number validation
INTEGER_CLASS = [REQUIRED, CHOICES, RANGE]
FLOAT_CLASS = [REQUIRED, CHOICES, RANGE]

# Dictionary validation
DICTIONARY_CLASS = [REQUIRED, VALIDATION]

# List validation
LIST_CLASS = [REQUIRED, MAX_LENGTH, MIN_LENGTH, ITEM, VALIDATION, UNIQUE,
              DATE_FORMAT]

# Tuple validation
TUPLE_CLASS = [REQUIRED, MAX_LENGTH, MIN_LENGTH, ITEM, VALIDATION, UNIQUE,
               DATE_FORMAT]

# Set validation
SET_CLASS = [REQUIRED, MAX_LENGTH, MIN_LENGTH, ITEM, VALIDATION, DATE_FORMAT]

# Boolean validation
BOOLEAN_CLASS = [REQUIRED]

# UUID Validation
UUID_CLASS = [REQUIRED]

# Email validation
EMAIL_CLASS = [REQUIRED, REGEX]

# Phone validation
PHONE_CLASS = [REQUIRED, MAX_LENGTH, MIN_LENGTH, REGEX]

# Password validation
PASSWORD_CLASS = [REQUIRED, MAX_LENGTH, MIN_LENGTH, REGEX]

# DateTime validation
DATE_TIME_CLASS = [REQUIRED, DATE_FORMAT]

# Regex validation
REGEX_CLASS = [REQUIRED, REGEX]
