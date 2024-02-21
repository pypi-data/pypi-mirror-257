class NoSuchEnvironmentError(Exception):
    """
    Raised then looking for an environment that does not exist in the
        Cringe Config.
    """

    message = "There is no '{}' environment in the provided config file."

    def __init__(self, environment_name):
        formatted_message = self.message.format(environment_name)

        super().__init__(formatted_message)
