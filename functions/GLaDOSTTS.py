from .util.ToolFunction import *

DEFAULT_NAME = "gladosTTS"
DEFAULT_DESCRIPTION = "converts AI message from text to speach, and speaks to the user"

class GLaDOSTTS(ToolFunction):
    def __init__(self, name=DEFAULT_NAME, description=DEFAULT_DESCRIPTION):
        super().__init__(name, description)
        self.add_parameter("message", "string", "The response from the language model to be read by the TTS", required=True)
        self.openai_func_desc = self.create_function_dict()

    def run_function(self, message):
        print(f"SPEAKING: {message}")
        return f"I called the API succesfully. No action is required. Only tell the user the following message and nothing else: {message}"

# Usage example
# glados_tts_function = GLaDOSTTS("gladosTTS", "converts AI message from text to speach")
# print(glados_tts_function.create_function_dict())