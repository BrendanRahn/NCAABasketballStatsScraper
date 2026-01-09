from pydantic import BaseModel

class GameResult(BaseModel):
    team_score: int
    opp_score: int
    result: str
    overtime: int