from key import HA_API_KEY, HA_URL
from hassapi import Hass

from .util.ToolFunction import *

DEFAULT_NAME = "turn_on_entity"
DEFAULT_DESCRIPTION = "turn on an entity in home assitant, like a tv or stero system"

class TurnOnEntity(ToolFunction):
    def __init__(self, name=DEFAULT_NAME, description=DEFAULT_DESCRIPTION):
        super().__init__(name, description)
        self.add_parameter("entity", "string", "The home assitant entity", required=True)
        self.openai_func_desc = self.create_function_dict()

    def run_function(self, entity: str) -> float:
        ha_client = Hass(HA_URL, HA_API_KEY, verify=False, timeout=10)
        current_entity = ha_client.get_state(entity)
        if current_entity.state == "off":
            ha_client.turn_on(entity)
            return "The entity was turned on"
        return "the entity was not turned on"