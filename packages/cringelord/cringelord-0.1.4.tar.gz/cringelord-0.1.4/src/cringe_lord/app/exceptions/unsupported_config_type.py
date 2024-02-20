from cringe_lord.app.exceptions.single_argument_formatted_message import (
    SingleArgumentFormattedMessageException
)


class UnsupportedConfigTypeError(SingleArgumentFormattedMessageException):
    """
    Raised when the provided config file is of an unsupported type.
    """
    message = """
    The config file you've provided is of an unsupported type. 
    Supported types:
        - Path to YAML file.
        - YAML file.
        - Dictionary.
        
    Your config file: {}
    """
