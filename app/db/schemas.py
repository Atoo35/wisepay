# app/db/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    email: str
    oauth_token: str
    splitwise_id: int
    payman_id: Optional[int]  = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime] = None

