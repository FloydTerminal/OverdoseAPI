from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# Deployment schema for the list of deployments within a station
class DeploymentResponse(BaseModel):
    deployment_id: str
    station_id: str
    deployment_name: Optional[str] = None
    region: Optional[str] = None
    ip: Optional[str] = None
    version: Optional[str] = None
    created: datetime
    online: bool
    last_event: Optional[datetime] = None
    player_count: Optional[int] = 0
    config: Optional[dict] = {}


# Station request schema for creating a new station
class StationRequest(BaseModel):
    station_id: str
    station_name: str
    created: Optional[datetime] = None  # Automatically set if not provided
    config: Optional[dict] = {}


# Station response schema to include the list of deployments
class StationResponse(BaseModel):
    station_id: str
    station_name: str
    created: datetime
    deployments: List[DeploymentResponse] = []  # Empty list by default
    config: Optional[dict] = {}

    class Config:
        orm_mode = True  # Allows conversion from SQLAlchemy models
