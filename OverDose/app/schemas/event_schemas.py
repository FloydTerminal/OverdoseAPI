from pydantic import BaseModel # type: ignore
from datetime import datetime

class EventRequest(BaseModel):
    event_id: str
    title: str
    description: str
    station_id: str
    start_time: datetime
    duration: int
    public: bool
    signups_open: bool
