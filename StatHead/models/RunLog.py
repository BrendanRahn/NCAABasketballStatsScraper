from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class RunLog(BaseModel):
    run_log_uuid: UUID
    status: str
    timestamp: datetime
    team: str
    row_offset: int