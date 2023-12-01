from .util.ToolFunction import *
from key import GOOGLE_MAPS_API_KEY
import googlemaps


DEFAULT_NAME = "get_directions"
DEFAULT_DESCRIPTION = "Get directions and current traffic from source to destination"

import yfinance as yf


class Maps(ToolFunction):
    def __init__(self, name=DEFAULT_NAME, description=DEFAULT_DESCRIPTION):
        super().__init__(name, description)
        self.add_parameter("source", "string", "The starting point location", required=True)
        self.add_parameter("destination", "string", "The destination you are going to", required=True)
        self.add_parameter("mode", "string", "mode of transportation", required=False)
        self.openai_func_desc = self.create_function_dict()

    def run_function(self, source: str, destination: str, mode="driving") -> float:
        try:

            # print(f"INSIDE FUNCTION {source} to {destination}")
            gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

            # Use the API to get directions
            directions_result = gmaps.directions(source,
                                     destination,
                                     mode="driving")
            simplified_data = ""
            # Clean up directions data
            for route in directions_result:
                for leg in route['legs']:
                    # Extract the necessary information
                    route_string = (
                        f"Route: {route.get('summary', 'No summary available')}, "
                        f"Duration: {leg['duration']['text']}, "
                        f"Distance: {leg['distance']['text']}\n"
                    )
                    simplified_data += route_string
            return simplified_data

        except Exception as e:
            print(f"Caught exception: {type(e).__name__}, Message: {e}")
            return str(e)


def test_maps():
    maps = Maps()
    print(maps.run_function("Golden Gate Bridge", "Case Center"))

test_maps()
