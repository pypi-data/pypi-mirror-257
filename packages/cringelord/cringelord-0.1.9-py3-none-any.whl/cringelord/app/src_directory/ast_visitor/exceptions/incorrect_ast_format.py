from cringelord.app.exceptions.single_argument_formatted_message import (
    SingleArgumentFormattedMessageException
)


class IncorrectASTFormatError(SingleArgumentFormattedMessageException):
    message = "AST is not correctly formatted: {}."
