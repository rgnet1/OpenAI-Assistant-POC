from homeassistant_api import Client
import os
import json

# File to save the data
filename = 'home_assistant_data.json'

# Check if the file already exists
if os.path.exists(filename):
    print(f"File '{filename}' already exists. No new data will be written.")
else:
    from key import HA_URL, HA_API_KEY

    # Creating a client instance
    client = Client(HA_URL, HA_API_KEY)

    # Fetching states from Home Assistant
    states = client.get_states()
    # File does not exist, proceed to write data
    print(f"Creating new file '{filename}'.")
    ignore_list = ["update", "sun",]
    # Preparing data for JSON
    data = []
    for state in states:
        combined = state.entity_id
        split = combined.split('.')
        domain = split[0]
        if domain in ignore_list:
            continue
        entity_only = split[1]
    
        # Extracting friendly names (assuming it could be a list)
        friendly_names = state.attributes.get('friendly_name')
        if not isinstance(friendly_names, list):
            friendly_names = [friendly_names] if friendly_names else ['N/A']

        data.append({
            'domain': domain,
            'entity_id': entity_only,
            'combined': combined,
            'friendly_names': friendly_names
        })

    # Writing data to JSON file
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

    print(f"Data saved to {filename}")




# from key import HA_URL, HA_API_KEY
# from homeassistant_api import Client
# import csv

# from .util.ToolFunction import *

# DEFAULT_NAME = "turn_on_entity"
# DEFAULT_DESCRIPTION = "turn on an entity in home assitant, like a tv or stero system"

# class TurnOnEntity(ToolFunction):
#     def __init__(self, name=DEFAULT_NAME, description=DEFAULT_DESCRIPTION):
#         super().__init__(name, description)
#         self.add_parameter("entity", "string", "The home assitant entity", required=True)
#         self.openai_func_desc = self.create_function_dict()

#     def run_function(self, entity: str) -> float:
        
#         client = Client(HA_URL, HA_API_KEY)

#         # Fetching states from Home Assistant
#         states = client.get_states()

#         # Extracting unique domains
#         unique_domains = set(state.domain for state in states)