from cringe_lord.app.exceptions.single_argument_formatted_message import (
    SingleArgumentFormattedMessageException
)


class MissingSettingError(SingleArgumentFormattedMessageException):
    """
    Raised when a setting the application requires is not present in the
        config file.
    """
    message = "Your config is missing the '{}' settings."
