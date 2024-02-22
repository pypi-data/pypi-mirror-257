class InvalidCringeConfigPathError(Exception):
    message = "'{}' is not a valid Cringe Config path."

    def __init__(self, config_path):
        formatted_message = self.message.format(config_path)

        super().__init__(formatted_message)
