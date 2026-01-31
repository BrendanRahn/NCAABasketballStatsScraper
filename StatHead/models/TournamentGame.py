from pydantic import BaseModel
from datetime import datetime
    
class TournamentGame(BaseModel):
    team_name: str
    team_seed: int #ncaa_tourn_seed
    date: datetime
    game_location: str
    opp_name: str
    opp_seed: int #ncaa_tourn_seed_opp
    team_score: int | None
    opp_score: int | None
    result: str | None
    round: str
    region: str
    overtime: int | None