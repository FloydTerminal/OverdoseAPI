from pydantic import BaseModel # type: ignore
from typing import Optional

class DeploymentRequest(BaseModel):
    deployment_id: str
    deployment_name: Optional[str] = None
    station_id: str
    ip: Optional[str] = None
    version: Optional[str] = None
