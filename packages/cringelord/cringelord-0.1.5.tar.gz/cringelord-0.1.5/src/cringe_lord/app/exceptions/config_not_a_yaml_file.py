from cringe_lord.app.exceptions.single_argument_formatted_message import (
    SingleArgumentFormattedMessageException
)


class ConfigNotAYamlFileException(SingleArgumentFormattedMessageException):
    """
    Raised when the provided config file is not a YAML file.
    """
    message = "The config file you've provided is not a YAML file. File: {}"
