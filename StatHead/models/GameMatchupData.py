from pydantic import BaseModel
from datetime import datetime
    
class GameMatchupData(BaseModel):
    team_name: str
    date: datetime
    game_location: str
    opp_name: str
    team_score: int
    opp_score: int
    result: str
    overtime: int