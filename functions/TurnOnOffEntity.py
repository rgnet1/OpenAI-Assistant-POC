from key import HA_API_KEY, HA_URL
from homeassistant_api import Client

from .util.ToolFunction import *

DEFAULT_NAME = "turn_on_off_entity"
DEFAULT_DESCRIPTION = "Turn on or off an entity in home assitant, only for media_player domain."

class TurnOnOffEntity(ToolFunction):
    def __init__(self, name=DEFAULT_NAME, description=DEFAULT_DESCRIPTION):
        super().__init__(name, description)
        self.add_parameter("domain", "string", "The domain in your knowledge base", required=True)
        self.add_parameter("entity_id", "string", "The entity_id in your knowlege base")
        self.add_parameter("toggle", "boolean", "True if entity needs to turn on. False if entity needs to turn off")
        self.openai_func_desc = self.create_function_dict()

    def run_function(self, domain: str, entity_id:str, toggle:bool = False) -> float:
        
        client = Client(HA_URL, HA_API_KEY)
        entity_domain = client.get_domain(domain)
        combined_entity = f"{domain}.{entity_id}"
        print(f"Entity:{combined_entity}")
        try:
            if toggle:
                entity_domain.turn_on(entity_id=combined_entity)
                print(f"Turning Entity:{combined_entity} on")
                return f"the {domain} was turned on"
            
            entity_domain.turn_off(entity_id=combined_entity)
            print(f"Turning Entity:{combined_entity} off")
            return f"the {domain} was turned off"
        except Exception as e:
            print(e)
            print(f"Caught exception: {type(e).__name__}, Message: {e}")
            return "Failed. You need to first retrieve the endity id and domain from your knowledge base"