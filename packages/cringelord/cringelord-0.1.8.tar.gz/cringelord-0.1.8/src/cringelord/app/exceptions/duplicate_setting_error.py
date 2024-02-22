from cringelord.app.exceptions.single_argument_formatted_message import (
    SingleArgumentFormattedMessageException
)


class DuplicateSettingError(SingleArgumentFormattedMessageException):
    message = "Setting '{}' is already present in the environment."
