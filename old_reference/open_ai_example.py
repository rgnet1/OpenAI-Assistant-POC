class ToolFunction:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.parameters = {}
        self.required_params = []

    def add_parameter(self, name, param_type, description, enum=None, required=True):
        param_info = {"type": param_type, "description": description}
        if enum is not None:
            param_info["enum"] = enum
        self.parameters[name] = param_info
        if required:
            self.required_params.append(name)

    def create_function_dict(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": self.parameters,
                    "required": self.required_params
                }
            }
        }

class Weather(ToolFunction):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.add_parameter("location", "string", "The city and state e.g. San Francisco, CA", required=True)
        self.add_parameter("unit", "string", "Temperature unit", enum=["c", "f"], required=False)

# Example usage:
weather_function = Weather("getCurrentWeather", "Get the weather in location")
print(weather_function.create_function_dict())
