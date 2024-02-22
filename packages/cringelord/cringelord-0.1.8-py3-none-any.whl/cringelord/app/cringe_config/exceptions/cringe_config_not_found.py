class CringeConfigNotFoundError(Exception):
    message = "Cringe Config file '{}' not found."

    def __init__(self, config_path):
        formatted_message = self.message.format(config_path)

        super().__init__(formatted_message)
