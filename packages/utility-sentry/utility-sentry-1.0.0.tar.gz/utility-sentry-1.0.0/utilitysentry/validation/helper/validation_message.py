"""This module contain all the error message for validation component."""

# Initialization fail error message.
JSON_VALIDATION_FAIL = "Please insure that you have a valid JSON object."
ARGS_NOT_SUPPORT = "Positional arguments are not allowed, use keyword"\
    " arguments only."
ACCEPTED_PARAMS_FAIL_ERROR = "{0} class only accepts the following"\
    " parameters: {1}."
BOOL_DATATYPE_ERROR = "The value of '{0}' parameter should be a boolean."
OPTIONAL_INT_DATATYPE_ERROR = "The value of '{0}' parameter should be an"\
    " integer or None."
OPTIONAL_LIST_DATATYPE_ERROR = "The value of '{0}' parameter should be a"\
    " list or None."
OPTIONAL_TUPLE_DATATYPE_ERROR = "The value of '{0}' parameter should be a"\
    " tuple or None."
STR_OR_NONE_DATATYPE_ERROR = "The value of '{0}' parameter should be a"\
    " string or None."
STR_DATATYPE_ERROR = "The value of '{0}' parameter should be a string."
LENGTH_ERROR = "The length of parameter '{0}' should be {1}."
ITEM_PARAM_INITIALIZATION_FAIL = "The value for parameter '{0}' contains"\
    " value that do not match the acceptable values '{1}'."
VALIDATION_PARAM_INITIALIZE_FAIL = "The acceptable value of parameter"\
    " '{0}' must be of type '{1}'."
REQUIRED_PARAM_MISSING_ERROR = "Please ensure that you provide the"\
    " '{0}' parameter with datatype {1} when initializing the {2} validation"\
    " class to proceed."
ITEM_DATETIME_INITIALIZE_FAIL = "Please ensure that you provide the"\
    " 'date_format' parameter when initializing the 'item' as a datetime."
ITEM_UTILITY_INITIALIZE_FAIL = "Please ensure that you provide the"\
    " 'validation' parameter when initializing the 'item' as a validation."

# Validation fail error messages.
REQUIRED_VALIDATION_FAIL = "The '{0}' parameter is required but not provided."
DATATYPE_VALIDATION_FAIL = "The datatype of field '{0}' should be '{1}'."
MAX_LENGTH_VALIDATION_FAIL = "The '{0}' parameter exceeds the maximum length"\
    " of {1} characters."
MIN_LENGTH_VALIDATION_FAIL = "The '{0}' parameter value is less than the"\
    " minimum length of {1} characters."
CHOICES_VALIDATION_FAIL = "The '{0}' parameter value should be one of the"\
    " specified choices: {1}."
RANGE_VALIDATION_FAIL = "The '{0}' parameter value should be within the"\
    " specified range: {1}"
SPECIAL_CHARACTERS_VALIDATION_FAIL = "Special characters are not allowed in"\
    " the '{0}' field. Please use only alphanumeric characters."
UNIQUE_VALIDATION_FAIL = "The values provided for '{0}' must be unique."\
    " Duplicate values found: {1}"
DATE_FORMAT_VALIDATION_FAIL = "The value provided for '{0}' does not match"\
    " the specified date format '{1}'."
REGEX_VALIDATION_FAIL = "The value provided for '{0}' does not match the"\
    " specified regex pattern '{1}'."
ITEM_VALIDATION_FAIL = "The value provided for '{0}' contains items that"\
    " do not match the specified data type '{1}'."
UUID_VALIDATION_FAIL = "The value provided for '{0}' is not a valid UUID."
