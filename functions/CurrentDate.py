from .util.ToolFunction import *

DEFAULT_NAME = "get_date_time"
DEFAULT_DESCRIPTION = "Retrieve the current date, time, and day of the week"
from datetime import datetime


class CurrentDate(ToolFunction):
    def __init__(self, name=DEFAULT_NAME, description=DEFAULT_DESCRIPTION):
        super().__init__(name, description)
        # self.add_parameter("info", "string", "extra ", required=True)
        self.openai_func_desc = self.create_function_dict()

    def run_function(self) -> str:
        try:
            # Get the current date and time
            now = datetime.now()

            # Format the date, time, and day of the week into a string
            formatted_string = now.strftime("%Y-%m-%d %H:%M:%S, %A")
            note = "Make sure you formate your dates in terms of next week or tomorrow if the user asks about specific dates"
            return "Todays date and time is "+ formatted_string + note
        except Exception as e:
            print(e)
            print(f"Caught exception: {type(e).__name__}, Message: {e}")
            return str(e)
    