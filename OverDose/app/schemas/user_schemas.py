from pydantic import BaseModel # type: ignore
from typing import Optional

class UserRequest(BaseModel):
    user_id: str
    username: str
    discord_id: Optional[str] = None
    platform: str
