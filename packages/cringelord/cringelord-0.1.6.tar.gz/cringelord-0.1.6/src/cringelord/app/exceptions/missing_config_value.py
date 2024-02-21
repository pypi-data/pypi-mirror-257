class MissingConfigValueError(Exception):
    template = "The provided config does not contain the '{}' setting."

    def __init__(self, setting_name):
        message = self.template.format(setting_name)

        super().__init__(message)
