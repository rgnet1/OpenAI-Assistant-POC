from homeassistant_api import Client
from key import HA_API_KEY, HA_URL

from .util.ToolFunction import *

DEFAULT_NAME = "gladosTTS"
DEFAULT_DESCRIPTION = "converts AI message from text to speach, and speaks to the user"

class GLaDOSTTS(ToolFunction):
    def __init__(self, name=DEFAULT_NAME, description=DEFAULT_DESCRIPTION):
        super().__init__(name, description)
        self.add_parameter("message", "string", "The response from the language model to be read by the TTS", required=True)
        self.add_parameter("volume","number", "The volume the user wants the TTS to speak at", required=False)
        self.add_parameter("speaker_entity", "string", "The sppeaker you want to use to play the TTS audio", required=False)
        self.openai_func_desc = self.create_function_dict()

    def run_function(self, message, volume=9, speaker_entity="media_player.ramis_room_speaker", script_entity_id="set_volume_and_speak"):
        try:
            client = Client(HA_URL, HA_API_KEY, verify_ssl=False)
            script = client.get_domain("script")
            script_fields = {
                "tts_message": message,
                "tts_volume": volume,
                "speaker_entity_id": speaker_entity
            }
            # Dynamically call the script method using the entity ID
            script_method = getattr(script, script_entity_id)
            script_method(**script_fields)
            return f"Success. only print out to the user: {message} "
        except:
            return f"Failed. to turn the device on"
