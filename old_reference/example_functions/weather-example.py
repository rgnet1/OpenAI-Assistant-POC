from util.ToolFunction import *
import pytest

class Weather(ToolFunction):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.add_parameter("location", "string", "The city and state e.g. San Francisco, CA", required=True)
        self.add_parameter("unit", "string", "Temperature unit", enum=["c", "f"], required=False)

# Example usage:
@pytest
def test_weather_function_tool():
    weather_function = Weather("getCurrentWeather", "Get the weather in location")
    open_function_tool = weather_function.create_function_dict()
    expected_value = {
        "type": "function",
        "function": {
            "name": "getCurrentWeather",
            "description": "Get the weather in location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
                    "unit": {"type": "string", "description": "Temperature unit", "enum": ["c", "f"]}
                },
                "required": ["location"]
            }
        }
    }
    assert open_function_tool == expected_value


# params_weather = create_parameters()
# add_parameter(params_weather, "location", "string", "The city and state e.g. San Francisco, CA")
# add_parameter(params_weather, "unit", "string", "Temperature unit", ["c", "f"])
