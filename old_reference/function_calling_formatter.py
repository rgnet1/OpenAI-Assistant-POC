
def add_parameter(param_dict, name, param_type, description, enum=None):
    """
    Add a parameter to the parameters dictionary.

    :param param_dict: The existing parameters dictionary.
    :param name: Name of the parameter.
    :param param_type: Type of the parameter (e.g., 'string').
    :param description: Description of the parameter.
    :param enum: Optional list of valid values for the parameter.
    """
    param_info = {"type": param_type, "description": description}
    if enum is not None:
        param_info["enum"] = enum
    param_dict[name] = param_info
    return param_dict

def create_parameters():
    """
    Create and return a parameters dictionary.
    """
    params = {}
    # Add parameters as needed, for example:
    # add_parameter(params, "location", "string", "The city and state e.g. San Francisco, CA")
    # add_parameter(params, "unit", "string", "Temperature unit", ["c", "f"])
    return params


def create_function_dict(name, description, parameters, required=None):
    """
    Create a dictionary for a function with specified parameters.

    :param name: Name of the function.
    :param description: Description of the function.
    :param parameters: Dictionary of parameters.
    :param required: List of required parameters. If None, all parameters are considered required.
    :return: Dictionary in the specified format.
    """

    function_dict = {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required if required is not None else list(parameters.keys())
            }
        }
    }

    return function_dict


def test_function_calling_format():
    # Example usage:
    params_weather = create_parameters()
    add_parameter(params_weather, "location", "string", "The city and state e.g. San Francisco, CA")
    add_parameter(params_weather, "unit", "string", "Temperature unit", ["c", "f"])

    params_nickname = create_parameters()
    add_parameter(params_nickname, "location", "string", "The city and state e.g. San Francisco, CA")

    function1 = create_function_dict("getCurrentWeather", "Get the weather in location", params_weather)
    function2 = create_function_dict("getNickname", "Get the nickname of a city", params_nickname)

    from pprint import pprint
    pprint(function1)
    pprint(function2)


