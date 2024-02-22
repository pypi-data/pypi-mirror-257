class SingleArgumentFormattedMessageException(Exception):
    """
    Base exception class for all exceptions that contain:
        1. A message template.
        2. An argument to format into the message template.
    """
    message: str

    def __init__(self, argument):
        formatted_message = self.message.format(argument)

        super().__init__(formatted_message)
