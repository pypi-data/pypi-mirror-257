def sanitize_name(name):
    """
    Sanitize a given name to handle special characters not allowed in
        environment variable names.
    Args:
        name: The name to sanitize.

    Returns:
        A sanitized version of the setting name.
    """
    sanitized_name = name.strip()
    sanitized_name = sanitized_name.replace(' ', '_')
    sanitized_name = sanitized_name.replace('-', '_')
    sanitized_name = sanitized_name.replace('.', '_')

    return sanitized_name
