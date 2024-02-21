class NamedCallDetected(Exception):
    """
    Raised when we detect an env call that doesn't contain a specific name of
        the variable to return. This could occur when the script's writer
        created a wrapper around the environment.

    Examples:
        Specific call: os.getenv("my_string")
        Non-Specific call: os.getenv(var_name)
            In this case, var_name might be a parameter to the wrapper
                function.
    """
