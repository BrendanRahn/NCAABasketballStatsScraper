from pydantic import BaseModel
from datetime import datetime
    
class GameMatchupData(BaseModel):
    team_name_abbr: str
    date: datetime
    game_location: str
    opp_name_abbr: str
    team_score: int
    opp_score: int
    result: str
    overtime: int