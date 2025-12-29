from pydantic import BaseModel

class RunLog(BaseModel):
    RunLogId: int
    StartTime: str
    EndTime: str
    StartTeam: str
    StartOffset: int
    EndTeam: str
    EndOffset: int