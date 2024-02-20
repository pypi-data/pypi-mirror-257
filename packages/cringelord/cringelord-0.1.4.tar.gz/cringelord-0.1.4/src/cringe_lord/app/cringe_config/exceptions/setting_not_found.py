class SettingNotFoundError(Exception):
    message = "Could not find setting '{}'"

    def __init__(self, setting_name):
        formatted_message = self.message.format(setting_name)

        super().__init__(formatted_message)
