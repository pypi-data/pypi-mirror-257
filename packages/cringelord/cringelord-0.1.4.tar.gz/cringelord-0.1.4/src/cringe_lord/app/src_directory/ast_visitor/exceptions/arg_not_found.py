from cringe_lord.app.exceptions.single_argument_formatted_message import (
    SingleArgumentFormattedMessageException
)


class ArgNotFoundError(SingleArgumentFormattedMessageException):
    """Raised when the arg is not found in a call."""
    message = "No arg found at position {}."
