import json
from .util.ToolFunction import *
from sportsipy.nba.schedule import Schedule


DEFAULT_NAME = "get_nba_schedule"
DEFAULT_DESCRIPTION = "Get the schedule of basketball games for the NBA"


class NbaSchedule(ToolFunction):
    def __init__(self, name=DEFAULT_NAME, description=DEFAULT_DESCRIPTION):
        super().__init__(name, description)
        self.add_parameter("season", "string", "year of the season.EX: 23-24 season date should be 2024", required=False)
        self.add_parameter("team", "string", "The team abbreviation", required=True)
        self.openai_func_desc = self.create_function_dict()

    def run_function(self, team: str, season: str = "2024") -> float:
        try:
            print("SEASON:",season, "TEAM", team)
            schedule = Schedule(team, season)
            # Convert the schedule to a list of dictionaries using list comprehension
            schedule_list = [{
                "date": game.date,
                "opponent": game.opponent_abbr,
                "result": game.result
            } for game in schedule]

            # Now, you can serialize schedule_list to JSON
            json_schedule = json.dumps(schedule_list, indent=0)
            print(json_schedule)
            return json_schedule
        except Exception as e:
            print(f"Caught exception: {type(e).__name__}, Message: {e}")
            return str(e)
