from cringe_lord.app.exceptions.single_argument_formatted_message import (
    SingleArgumentFormattedMessageException
)


class NoSuchEnvironmentError(SingleArgumentFormattedMessageException):
    """
    Raised then looking for an environment that does not exist in the
        Cringe Config.
    """

    message = "There is no '{}' environment in the provided config file."
