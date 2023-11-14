from key import HA_API_KEY, HA_URL
from homeassistant_api import Client

from .util.ToolFunction import *

DEFAULT_NAME = "turn_on_off_entity"
DEFAULT_DESCRIPTION = "turn on or off an entity in home assitant, like a tv or stero system"

class TurnOnEntity(ToolFunction):
    def __init__(self, name=DEFAULT_NAME, description=DEFAULT_DESCRIPTION):
        super().__init__(name, description)
        self.add_parameter("combined_entity", "string", "This is the combine name of the entity in your knowledge base", required=True)
        self.add_parameter("toggle", "boolean", "True if entity needs to turn on. False if entity needs to turn off")
        self.openai_func_desc = self.create_function_dict()

    def run_function(self, combined_entity: str, toggle:bool = False) -> float:
        
        client = Client(HA_URL, HA_API_KEY)
        domain = combined_entity.split('.')[0]
        entity_domain = client.get_domain(domain)
        print(f"Entity:{combined_entity}")
        if toggle:
            entity_domain.turn_on(entity_id=combined_entity)
            return f"the {domain} was turned on"
        
        entity_domain.turn_off(entity_id=combined_entity)
        return f"the {domain} was turned on"