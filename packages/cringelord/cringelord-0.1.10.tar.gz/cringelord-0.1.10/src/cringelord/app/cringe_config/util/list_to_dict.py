from cringelord.app.cringe_config.exceptions import NoConversionRequired


def list_to_dict(list_):
    try:
        _validate_input(list_)
    except NoConversionRequired:
        return list_.copy()

    result = {}
    for dict_ in list_:
        _add_to_dict(input_dict=dict_, output_dict=result)

    return result


def _validate_input(list_):
    if isinstance(list_, dict):
        raise NoConversionRequired("Input is already a dictionary.")

    if not isinstance(list_, list):
        raise TypeError("Input should be a list.")


def _add_to_dict(input_dict, output_dict):
    if isinstance(input_dict, dict):
        output_dict.update(input_dict)
    elif isinstance(input_dict, str):
        output_dict.update({input_dict: None})
    else:
        raise TypeError("List items should be dictionaries.")
