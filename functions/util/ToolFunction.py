from abc import ABC, abstractmethod


class ToolFunction(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.parameters = {}
        self.required_params = []

    def add_parameter(self, name, param_type, description, enum=None, required=True):

        '''
        param_type: 
            string
            number
            boolean
            null/empty
            object
            array
        '''
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
    
    @abstractmethod
    def run_function(self, **kwargs):
        """Abstract method to run the tool's function. Must be overridden."""
        pass
