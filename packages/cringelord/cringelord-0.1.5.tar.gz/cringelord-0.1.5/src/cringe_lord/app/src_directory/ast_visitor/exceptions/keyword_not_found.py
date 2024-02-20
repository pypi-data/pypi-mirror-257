from cringe_lord.app.exceptions.single_argument_formatted_message import (
    SingleArgumentFormattedMessageException
)


class KeywordNotFoundError(SingleArgumentFormattedMessageException):
    message = "Keyword not found: '{}.'"
